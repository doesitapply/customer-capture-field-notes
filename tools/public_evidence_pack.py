#!/usr/bin/env python
"""Create a bounded, read-only evidence packet for one public web page.

This is an observation tool, not a compliance certification or security scan.
It retrieves a public HTTP(S) page, records limited public signals, and writes
JSON + Markdown evidence files that can be inspected or repeated later.
"""

from __future__ import annotations

import argparse
import hashlib
import ipaddress
import json
import re
import socket
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

USER_AGENT = "PublicEvidencePack/0.1 (+https://github.com/doesitapply/customer-capture-field-notes)"
MAX_BODY_BYTES = 2_000_000
TIMEOUT_SECONDS = 15


class EvidencePackError(ValueError):
    """Raised when a requested URL is outside this tool's public-page boundary."""


def _public_ip(address: str) -> bool:
    candidate = ipaddress.ip_address(address)
    return candidate.is_global


def assert_public_url(value: str) -> urllib.parse.ParseResult:
    parsed = urllib.parse.urlparse(value)
    if parsed.scheme not in {"http", "https"}:
        raise EvidencePackError("URL must start with http:// or https://")
    if not parsed.hostname:
        raise EvidencePackError("URL must include a public hostname")
    if parsed.username or parsed.password:
        raise EvidencePackError("URLs with embedded credentials are not allowed")
    host = parsed.hostname.rstrip(".").lower()
    if host == "localhost" or host.endswith(".localhost"):
        raise EvidencePackError("local/private hosts are not allowed")
    try:
        addresses = {info[4][0] for info in socket.getaddrinfo(host, None)}
    except socket.gaierror as exc:
        raise EvidencePackError(f"cannot resolve host {host!r}: {exc}") from exc
    if not addresses or any(not _public_ip(address) for address in addresses):
        raise EvidencePackError("host resolves to a non-public address")
    return parsed


class SafeRedirectHandler(urllib.request.HTTPRedirectHandler):
    """Reject redirects away from the public-internet boundary."""

    def redirect_request(self, req: Any, fp: Any, code: int, msg: str, headers: Any, newurl: str) -> Any:
        assert_public_url(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


@dataclass
class PageSignals:
    title: str | None
    meta_description: str | None
    headings_h1: list[str]
    forms: int
    visible_input_controls: int
    labels_with_for: int
    privacy_link_detected: bool
    terms_link_detected: bool
    cookie_text_detected: bool
    links_sample: list[dict[str, str]]


class PublicPageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title_parts: list[str] = []
        self.h1s: list[list[str]] = []
        self._inside_title = False
        self._active_h1: list[str] | None = None
        self.forms = 0
        self.visible_input_controls = 0
        self.labels_with_for = 0
        self._links: list[dict[str, str]] = []
        self._legal_cues: list[str] = []
        self._active_link: dict[str, str] | None = None
        self.visible_text: list[str] = []
        self.meta_description: str | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key.lower(): (value or "") for key, value in attrs}
        tag = tag.lower()
        if tag == "title":
            self._inside_title = True
        elif tag == "h1":
            self._active_h1 = []
        elif tag == "form":
            self.forms += 1
        elif tag in {"input", "textarea", "select"}:
            control_type = values.get("type", "text").lower()
            if control_type not in {"hidden", "submit", "button", "reset", "image"}:
                self.visible_input_controls += 1
        elif tag == "label" and values.get("for"):
            self.labels_with_for += 1
        elif tag == "meta" and values.get("name", "").lower() == "description":
            self.meta_description = values.get("content") or self.meta_description
        elif tag == "a" and values.get("href"):
            self._active_link = {"href": values["href"], "text": ""}

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag == "title":
            self._inside_title = False
        elif tag == "h1" and self._active_h1 is not None:
            self.h1s.append(self._active_h1)
            self._active_h1 = None
        elif tag == "a" and self._active_link is not None:
            self._legal_cues.append(
                f"{self._active_link['href']} {self._active_link['text']}"
            )
            if len(self._links) < 40:
                self._links.append(self._active_link)
            self._active_link = None

    def handle_data(self, data: str) -> None:
        compact = " ".join(data.split())
        if not compact:
            return
        self.visible_text.append(compact)
        if self._inside_title:
            self.title_parts.append(compact)
        if self._active_h1 is not None:
            self._active_h1.append(compact)
        if self._active_link is not None:
            self._active_link["text"] += (" " if self._active_link["text"] else "") + compact

    def signals(self) -> PageSignals:
        links = [
            {"href": item["href"], "text": " ".join(item["text"].split())[:160]}
            for item in self._links
        ]
        legal_blob = " ".join(self._legal_cues).lower()
        body_blob = " ".join(self.visible_text).lower()
        return PageSignals(
            title=" ".join(self.title_parts) or None,
            meta_description=self.meta_description,
            headings_h1=[" ".join(parts) for parts in self.h1s if " ".join(parts)],
            forms=self.forms,
            visible_input_controls=self.visible_input_controls,
            labels_with_for=self.labels_with_for,
            privacy_link_detected=bool(re.search(r"privacy", legal_blob)),
            terms_link_detected=bool(re.search(r"terms|conditions", legal_blob)),
            cookie_text_detected="cookie" in body_blob,
            links_sample=links,
        )


def fetch_public_page(url: str) -> dict[str, Any]:
    assert_public_url(url)
    opener = urllib.request.build_opener(SafeRedirectHandler())
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "text/html,application/xhtml+xml"})
    try:
        with opener.open(request, timeout=TIMEOUT_SECONDS) as response:
            raw = response.read(MAX_BODY_BYTES + 1)
            if len(raw) > MAX_BODY_BYTES:
                raise EvidencePackError(f"response exceeds {MAX_BODY_BYTES:,} byte read-only cap")
            final_url = response.geturl()
            assert_public_url(final_url)
            content_type = response.headers.get_content_type()
            charset = response.headers.get_content_charset() or "utf-8"
            decoded = raw.decode(charset, errors="replace")
            headers = {key.lower(): value for key, value in response.headers.items()}
            return {
                "requested_url": url,
                "final_url": final_url,
                "status_code": getattr(response, "status", None),
                "content_type": content_type,
                "charset": charset,
                "headers": headers,
                "raw": raw,
                "body": decoded,
            }
    except urllib.error.HTTPError as exc:
        raise EvidencePackError(f"HTTP {exc.code} while retrieving public URL") from exc
    except urllib.error.URLError as exc:
        raise EvidencePackError(f"network failure while retrieving public URL: {exc.reason}") from exc


def build_packet(url: str) -> dict[str, Any]:
    fetched = fetch_public_page(url)
    parser = PublicPageParser()
    if fetched["content_type"] in {"text/html", "application/xhtml+xml"}:
        parser.feed(fetched["body"])
        parser.close()
    observed_headers = {
        key: fetched["headers"].get(key)
        for key in [
            "content-security-policy",
            "strict-transport-security",
            "x-content-type-options",
            "x-frame-options",
            "referrer-policy",
            "permissions-policy",
        ]
        if fetched["headers"].get(key)
    }
    return {
        "tool": "Public Evidence Pack",
        "version": "0.1",
        "observed_at_utc": datetime.now(timezone.utc).isoformat(),
        "boundary": "Read-only observation of one public URL. Not a compliance certification, accessibility conformance test, penetration test, legal opinion, or outcome guarantee.",
        "retrieval": {
            "requested_url": fetched["requested_url"],
            "final_url": fetched["final_url"],
            "status_code": fetched["status_code"],
            "content_type": fetched["content_type"],
            "bytes_read": len(fetched["raw"]),
            "sha256": hashlib.sha256(fetched["raw"]).hexdigest(),
        },
        "http_header_observations": observed_headers,
        "page_observations": asdict(parser.signals()),
        "not_checked": [
            "Authenticated pages, private data, forms, or checkout flows",
            "JavaScript-rendered behavior or API calls",
            "Accessibility conformance against WCAG",
            "Security vulnerabilities, exploitability, or penetration testing",
            "Legal, regulatory, privacy, or certification compliance",
            "Business conversion, revenue, or performance outcomes",
        ],
    }


def render_markdown(packet: dict[str, Any]) -> str:
    retrieval = packet["retrieval"]
    page = packet["page_observations"]
    headers = packet["http_header_observations"]
    lines = [
        "# Public Evidence Pack",
        "",
        f"- **Observed:** {packet['observed_at_utc']}",
        f"- **Requested URL:** {retrieval['requested_url']}",
        f"- **Final URL:** {retrieval['final_url']}",
        f"- **HTTP status:** {retrieval['status_code']}",
        f"- **Content hash (SHA-256):** `{retrieval['sha256']}`",
        "",
        "## Boundary",
        "",
        packet["boundary"],
        "",
        "## Public page observations",
        "",
        f"- Title: {page['title'] or 'not detected'}",
        f"- Meta description: {page['meta_description'] or 'not detected'}",
        f"- H1 headings: {', '.join(page['headings_h1']) or 'none detected'}",
        f"- Forms: {page['forms']}",
        f"- Visible input controls: {page['visible_input_controls']}",
        f"- Labels with `for` attributes: {page['labels_with_for']}",
        f"- Privacy-link cue detected: {'yes' if page['privacy_link_detected'] else 'no'}",
        f"- Terms-link cue detected: {'yes' if page['terms_link_detected'] else 'no'}",
        f"- Cookie text detected: {'yes' if page['cookie_text_detected'] else 'no'}",
        "",
        "## HTTP header observations",
        "",
    ]
    if headers:
        lines.extend(f"- `{key}`: `{value}`" for key, value in headers.items())
    else:
        lines.append("- No selected response-header observations were present in this retrieval.")
    lines.extend(["", "## Not checked", ""])
    lines.extend(f"- {item}" for item in packet["not_checked"])
    return "\n".join(lines) + "\n"


def write_packet(packet: dict[str, Any], output_dir: Path) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "public-evidence-pack.json"
    markdown_path = output_dir / "public-evidence-pack.md"
    json_path.write_text(json.dumps(packet, indent=2) + "\n", encoding="utf-8")
    markdown_path.write_text(render_markdown(packet), encoding="utf-8")
    return json_path, markdown_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url", help="One public http(s) URL to observe")
    parser.add_argument("--out", default="evidence-output", help="Directory for JSON and Markdown output")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        packet = build_packet(args.url)
        json_path, markdown_path = write_packet(packet, Path(args.out))
    except EvidencePackError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(f"Wrote {json_path}")
    print(f"Wrote {markdown_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
