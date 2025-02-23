import os
import re
from typing import Dict
from typing import List


def get_changed_files() -> List[str]:
    """
    Get the list of changed files from the environment variable.
    The environment variable CHANGED_FILES is a space-separated string.

    Returns:
        List[str]: List of changed files
    """
    changed_files_str = os.getenv("CHANGED_FILES")
    if not changed_files_str:
        print("CHANGED_FILES is not set.")
        return []

    changed_files = changed_files_str.strip().split(" ")
    return changed_files


def parse_annotation(content: str) -> Dict[str, int]:
    """Parse the annotation from the GitHub Actions output.

    Example annotation:
    ::error title=Ruff (F821),file=/Developer/chatbot/backend/app/main.py,line=51,col=23,endLine=51,endColumn=32::backend/app/main.py:51:23: F821 Undefined name `Constants`
    """
    changed_files = get_changed_files()
    stats = {}
    for files in changed_files:
        stats[files] = {"error": 0, "warning": 0}

    for line in content.strip().split("\n"):
        match = re.search(r"file=([^,]+)", line)
        if not match:
            continue

        # Take the file path
        full_path = match.group(1)
        path = full_path.split("chatbot/")[-1]

        # Count error/warning
        if not stats.get(path):
            stats[path] = {"error": 0, "warning": 0}
        else:
            if "error" in line:
                stats[path]["error"] += 1
            elif "warning" in line:
                stats[path]["warning"] += 1

    return stats


def generate_markdown_report(stats):
    total_files = len(stats)
    files_with_issues = sum(1 for s in stats.values() if s["error"] > 0 or s["warning"] > 0)
    clean_files = total_files - files_with_issues

    # Report header
    report = [f"### 🚧 Python linting status: {clean_files}/{total_files}\n"]

    # If there are no errors/warnings, return the report
    if files_with_issues == 0:
        return "\n".join(report + ["All files are clean! 🎉"])

    # Else, loop through the stats and generate the report
    report.extend(
        ["| File | Status | Warnings | Errors |", "|------|--------|----------|---------|"]
    )
    for file_path, counts in stats.items():
        status = "✅" if counts["error"] == 0 and counts["warning"] == 0 else "❌"
        row = f"| {file_path} | {status} | {counts['warning']} | {counts['error']} |"
        report.append(row)

    return "\n".join(report)


def main():
    with open("annotations.txt") as f:
        content = f.read()

    stats = parse_annotation(content)
    report = generate_markdown_report(stats)
    print(report)


if __name__ == "__main__":
    main()
