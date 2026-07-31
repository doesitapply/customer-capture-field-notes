#!/usr/bin/env python
"""Read-only monitor for public GitHub teardown-request issues.

The monitor checks only one repository's public Issues endpoint, filters for a
single label, and emits a compact JSON handoff. It never authenticates, writes,
replies, labels, closes, assigns, or opens an issue. Issue text is deliberately
not copied into the output: it is untrusted public input and must be reviewed in
its original public context by a human before any scope, price, or payment step.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

API_ROOT = "https://api.github.com"
DEFAULT_REPO = "doesitapply/customer-capture-field-notes"
DEFAULT_LABEL = "public-only-teardown"
DEFAULT_LIMIT = 20
MAX_LIMIT = 100
REPO_PATTERN = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")


class IntakeCheckError(ValueError):
    """Expected, safe failure of the read-only monitor."""


@dataclass(frozen=True)
class PublicRequest:
    number: int
    created_at: str | None
    html_url: str


def validate_repo(value: str) -> str:
    if not REPO_PATTERN.fullmatch(value):
        raise IntakeCheckError("repo must have the form owner/repository")
    return value


def validate_label(value: str) -> str:
    if not value or len(value) > 100 or any(ord(char) < 32 for char in value):
        raise IntakeCheckError("label must be a non-empty printable string up to 100 characters")
    return value


def build_issues_url(repo: str, label: str, limit: int) -> str:
    validate_repo(repo)
    validate_label(label)
    if not 1 <= limit <= MAX_LIMIT:
        raise IntakeCheckError(f"limit must be between 1 and {MAX_LIMIT}")
    query = urllib.parse.urlencode({"state": "open", "labels": label, "per_page": str(limit)})
    return f"{API_ROOT}/repos/{repo}/issues?{query}"


def fetch_issue_rows(url: str) -> list[dict[str, Any]]:
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "PublicIntakeMonitor/0.1 (+https://github.com/doesitapply/customer-capture-field-notes)",
            "X-GitHub-Api-Version": "2022-11-28",
        },
        method="GET",
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            payload = json.load(response)
    except urllib.error.HTTPError as exc:
        raise IntakeCheckError(f"GitHub API returned HTTP {exc.code}") from exc
    except urllib.error.URLError as exc:
        raise IntakeCheckError(f"GitHub API network failure: {exc.reason}") from exc
    except json.JSONDecodeError as exc:
        raise IntakeCheckError("GitHub API response was not valid JSON") from exc
    if not isinstance(payload, list) or not all(isinstance(item, dict) for item in payload):
        raise IntakeCheckError("GitHub API response was not an issue-list array")
    return payload


def has_requested_label(item: dict[str, Any], label: str) -> bool:
    labels = item.get("labels", [])
    return any(isinstance(entry, dict) and entry.get("name") == label for entry in labels)


def normalize_requests(rows: list[dict[str, Any]], label: str) -> list[PublicRequest]:
    requests: list[PublicRequest] = []
    for item in rows:
        # GitHub's Issues API can include pull requests; do not treat one as an inbound request.
        if "pull_request" in item or not has_requested_label(item, label):
            continue
        number = item.get("number")
        html_url = item.get("html_url")
        if not isinstance(number, int) or not isinstance(html_url, str) or not html_url.startswith("https://github.com/"):
            continue
        created_at = item.get("created_at") if isinstance(item.get("created_at"), str) else None
        requests.append(PublicRequest(number=number, created_at=created_at, html_url=html_url))
    return requests


def build_result(repo: str, label: str, limit: int, rows: list[dict[str, Any]]) -> dict[str, Any]:
    source_url = build_issues_url(repo, label, limit)
    requests = normalize_requests(rows, label)
    status = "WAITING_EXTERNAL" if not requests else "HUMAN_SCOPE_REVIEW_REQUIRED"
    next_action = (
        "No public teardown request is waiting. Do not manufacture outreach or a payment request; re-run before any new send or reply."
        if not requests
        else "A public request exists. A human must review the original public issue, confirm public-only scope, and decide whether to offer the $99 teardown; this tool does not reply or charge."
    )
    return {
        "tool": "Public Intake Monitor",
        "version": "0.1",
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "side_effect_class": "read_only_public_api_get",
        "status": status,
        "source": {
            "provider": "GitHub public Issues API",
            "query_url": source_url,
            "repo": repo,
            "label": label,
            "per_page_limit": limit,
        },
        "result": {
            "matching_open_request_count": len(requests),
            "requests": [request.__dict__ for request in requests],
            "issue_text_handling": "not copied; original issue must be reviewed as untrusted public input",
        },
        "next_action": next_action,
        "hard_stops": [
            "No authentication, account changes, issue writes, replies, labels, assignments, or closures",
            "No automatic scope approval, payment request, payment link, or public outreach",
            "No private, customer, financial, login, or sensitive data should be requested or copied into a public issue",
        ],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=DEFAULT_REPO, help="Public GitHub repository in owner/repository form")
    parser.add_argument("--label", default=DEFAULT_LABEL, help="Exact issue label to monitor")
    parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT, help=f"Maximum open issue rows to query (1-{MAX_LIMIT})")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        url = build_issues_url(args.repo, args.label, args.limit)
        rows = fetch_issue_rows(url)
        result = build_result(args.repo, args.label, args.limit, rows)
    except IntakeCheckError as exc:
        print(json.dumps({"status": "BLOCKED_SAFE", "error_class": "intake_check_error", "error": str(exc)}), file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
