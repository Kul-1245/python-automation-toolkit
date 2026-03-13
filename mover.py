# =============================================================================
# toolkit/mover.py
# Feature 4: Auto-Move Files by Rules
#
# Automatically moves files from a source folder to pre-defined destination
# folders based on customisable rules.  Rules can match by:
#   - extension  : move all .pdf files to a target folder
#   - prefix     : move files whose name starts with a given string
#   - suffix     : move files whose name ends with a given string (before ext)
#   - contains   : move files whose name includes a given substring
#   - size_above : move files larger than N bytes
#   - size_below : move files smaller than N bytes
#
# Rules are evaluated in order; the first matching rule wins.
# =============================================================================

import os
from pathlib import Path
from typing import Optional

from utils.file_utils import human_readable_size, list_files, safe_move
from utils.logger import get_logger

logger = get_logger("mover")


# ---------------------------------------------------------------------------
# Rule builder helpers
# Use these functions to create clean rule dictionaries.
# ---------------------------------------------------------------------------

def rule_by_extension(extension: str, dest: str) -> dict:
    """Move files that have a specific extension. e.g. '.pdf'"""
    return {"type": "extension", "value": extension.lower(), "dest": dest}


def rule_by_prefix(prefix: str, dest: str) -> dict:
    """Move files whose name starts with the given prefix."""
    return {"type": "prefix", "value": prefix, "dest": dest}


def rule_by_suffix(suffix: str, dest: str) -> dict:
    """Move files whose stem ends with the given suffix (before the extension)."""
    return {"type": "suffix", "value": suffix, "dest": dest}


def rule_by_contains(substring: str, dest: str) -> dict:
    """Move files whose name contains the given substring."""
    return {"type": "contains", "value": substring, "dest": dest}


def rule_by_size_above(min_bytes: int, dest: str) -> dict:
    """Move files that are larger than min_bytes."""
    return {"type": "size_above", "value": min_bytes, "dest": dest}


def rule_by_size_below(max_bytes: int, dest: str) -> dict:
    """Move files that are smaller than max_bytes."""
    return {"type": "size_below", "value": max_bytes, "dest": dest}


# ---------------------------------------------------------------------------
# Core logic
# ---------------------------------------------------------------------------

def _matches_rule(filepath: str, rule: dict) -> bool:
    """
    Checks whether a file matches a single rule.

    Args:
        filepath: Full path to the file.
        rule:     Rule dictionary created by one of the rule_by_* helpers.

    Returns:
        True if the file matches the rule, False otherwise.
    """
    path_obj = Path(filepath)
    rule_type = rule.get("type", "")
    value     = rule.get("value", "")

    if rule_type == "extension":
        return path_obj.suffix.lower() == value

    elif rule_type == "prefix":
        return path_obj.name.startswith(value)

    elif rule_type == "suffix":
        return path_obj.stem.endswith(value)

    elif rule_type == "contains":
        return value in path_obj.name

    elif rule_type == "size_above":
        return os.path.getsize(filepath) > value

    elif rule_type == "size_below":
        return os.path.getsize(filepath) < value

    else:
        logger.warning(f"Unknown rule type '{rule_type}' — skipping.")
        return False


def auto_move(
    source_dir: str,
    rules: list[dict],
    dry_run: bool = False,
) -> dict[str, list[str]]:
    """
    Moves files from source_dir to destination folders based on rules.

    Args:
        source_dir: Folder to scan for files.
        rules:      Ordered list of rule dicts (first match wins).
        dry_run:    Preview without actually moving any files.

    Returns:
        A summary dict: { destination_folder: [list_of_moved_files] }
    """
    if not rules:
        logger.error("No rules provided. Pass at least one rule dict.")
        return {}

    logger.info(f"{'[DRY RUN] ' if dry_run else ''}Auto-move from '{source_dir}' with {len(rules)} rule(s).")

    files = list_files(source_dir, recursive=False)
    if not files:
        logger.warning(f"No files found in '{source_dir}'.")
        return {}

    summary: dict[str, list] = {}
    unmatched: list[str] = []

    for filepath in files:
        path_obj = Path(filepath)
        matched  = False

        for rule in rules:
            if _matches_rule(filepath, rule):
                dest_dir = rule["dest"]
                summary.setdefault(dest_dir, [])

                if dry_run:
                    logger.info(f"  [WOULD MOVE] '{path_obj.name}' → '{dest_dir}'")
                    summary[dest_dir].append(path_obj.name)
                else:
                    result = safe_move(filepath, dest_dir)
                    if result:
                        logger.info(f"  Moved '{path_obj.name}' → '{dest_dir}'")
                        summary[dest_dir].append(path_obj.name)

                matched = True
                break  # First rule wins; stop checking remaining rules

        if not matched:
            unmatched.append(path_obj.name)

    _print_move_summary(summary, unmatched, dry_run)
    return summary


def _print_move_summary(summary: dict, unmatched: list, dry_run: bool) -> None:
    """Prints a tidy breakdown of where files were (or would be) moved."""
    print("\n" + "=" * 65)
    print(f"  {'DRY RUN — ' if dry_run else ''}Auto-Move Summary")
    print("=" * 65)

    if not summary:
        print("  No files matched any rule.")
    else:
        total = 0
        for dest, files in sorted(summary.items()):
            count = len(files)
            total += count
            print(f"  📁 {dest}")
            for f in files:
                print(f"       • {f}")
        print(f"\n  Total moved: {total} file(s)")

    if unmatched:
        print(f"\n  ⚠ Unmatched (no rule applied): {len(unmatched)} file(s)")
        for f in unmatched:
            print(f"     • {f}")

    print("=" * 65 + "\n")
