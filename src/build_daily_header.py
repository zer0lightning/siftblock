#!/usr/bin/env python3
"""
Build the header for blocklist.txt's daily diff file. Used by the daily-diff
GitHub Actions workflow — kept as a real script file (not an inline heredoc)
so it can't break on YAML/indentation quirks and can be tested directly.

Usage: build_daily_header.py DATE NEW_COUNT
"""

import sys
from datetime import datetime, timezone

REPO_URL = "https://github.com/zer0lightning/siftblock"


def build_daily_header(date: str, new_count: str) -> str:
    now = datetime.now(timezone.utc)
    last_modified = now.strftime("%d %b %Y %H:%M UTC")
    return (
        "# Title: SiftBlock Daily New Entries\n"
        f"# Date: {date}\n"
        "# Description: Domains newly observed today vs the previous day.\n"
        f"# Homepage: {REPO_URL}\n"
        f"# License: {REPO_URL}/blob/main/DISCLAIMER.md\n"
        f"# Issues: {REPO_URL}/issues\n"
        f"# Last modified: {last_modified}\n"
        f"# Number of new entries: {new_count}\n"
        "#\n"
    )


def main() -> None:
    if len(sys.argv) != 3:
        print("usage: build_daily_header.py DATE NEW_COUNT", file=sys.stderr)
        sys.exit(1)
    sys.stdout.write(build_daily_header(sys.argv[1], sys.argv[2]))


if __name__ == "__main__":
    main()
