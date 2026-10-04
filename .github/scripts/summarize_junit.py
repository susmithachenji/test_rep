"""Render the pytest JUnit XML as a markdown block in the GitHub job summary.

Writes to the file pointed at by ``GITHUB_STEP_SUMMARY`` (or stdout locally).
"""

from __future__ import annotations

import os
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

JUNIT = Path(os.environ.get("JUNIT_FILE", "reports/junit.xml"))
LABEL = os.environ.get("JOB_LABEL", "pytest")
MAX_LISTED = 25


def main() -> int:
    if not JUNIT.exists():
        message = f"### {LABEL}\n\nNo JUnit report found at `{JUNIT}` - pytest did not finish."
        return _write(message)

    root = ET.parse(JUNIT).getroot()
    suites = [root] if root.tag == "testsuite" else root.findall("testsuite")

    total = failures = errors = skipped = 0
    duration = 0.0
    problems: list[str] = []

    for suite in suites:
        total += int(suite.get("tests", 0))
        failures += int(suite.get("failures", 0))
        errors += int(suite.get("errors", 0))
        skipped += int(suite.get("skipped", 0))
        duration += float(suite.get("time", 0) or 0)
        for case in suite.iter("testcase"):
            problem = case.find("failure") if case.find("failure") is not None else case.find("error")
            if problem is not None:
                problems.append(f"- `{case.get('classname')}` › `{case.get('name')}`")

    status = "✅ passed" if not failures and not errors else "❌ failed"
    lines = [
        f"### {LABEL}: {status}",
        "",
        f"| passed | failed | errors | skipped | duration |",
        "| --- | --- | --- | --- | --- |",
        f"| {total - failures - errors - skipped} | {failures} | {errors} | {skipped} | {duration:.1f}s |",
        "",
        "Download the HTML report and failure screenshots from the *Artifacts* section of this run.",
        "",
    ]
    if problems:
        lines.append(f"**Failing tests** (showing up to {MAX_LISTED}):")
        lines.append("")
        lines.extend(problems[:MAX_LISTED])

    return _write("\n".join(lines))


def _write(markdown: str) -> int:
    summary_file = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_file:
        with open(summary_file, "a", encoding="utf-8") as handle:
            handle.write(markdown + "\n")
    else:
        print(markdown)
    return 0


if __name__ == "__main__":
    sys.exit(main())