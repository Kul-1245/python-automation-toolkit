#!/usr/bin/env python3
# =============================================================================
# main.py  —  Python Automation Toolkit
# =============================================================================
# This is the main entry point for the toolkit.
# Run it directly and choose which feature to use from the interactive menu,
# OR import individual modules in your own scripts for programmatic use.
#
# Usage:
#   python main.py
#
# =============================================================================

import os
import sys

# Make sure Python can find our local packages regardless of where main.py is run from
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from toolkit.organizer    import organize_folder
from toolkit.renamer      import bulk_rename
from toolkit.deduplicator import remove_duplicates
from toolkit.mover        import (
    auto_move,
    rule_by_extension,
    rule_by_prefix,
    rule_by_contains,
    rule_by_size_above,
)
from utils.logger import get_logger

logger = get_logger("main")

# ---------------------------------------------------------------------------
# ASCII banner
# ---------------------------------------------------------------------------
BANNER = r"""
 ____        _   _                        _    _ _ _   _
|  _ \ _   _| |_| |__   ___  _ __       / \  | (_) |_| | __
| |_) | | | | __| '_ \ / _ \| '_ \     / _ \ | | | __| |/ /
|  __/| |_| | |_| | | | (_) | | | |   / ___ \| | | |_|   <
|_|    \__, |\__|_| |_|\___/|_| |_|  /_/   \_\_|_|\__|_|\_\
       |___/
 _____           _ _    _ _
|_   _|__   ___ | | | _(_) |_
  | |/ _ \ / _ \| | |/ / | __|
  | | (_) | (_) | |   <| | |_
  |_|\___/ \___/|_|_|\_\_|\__|
"""


def print_menu() -> None:
    """Prints the interactive feature menu."""
    print(BANNER)
    print("  What would you like to do?\n")
    print("  [1]  Organise files by type  (Images, Videos, Documents …)")
    print("  [2]  Bulk rename files")
    print("  [3]  Remove duplicate files")
    print("  [4]  Auto-move files by rules")
    print("  [5]  Run demo  (creates sample files & runs all features)")
    print("  [0]  Exit\n")


def get_directory(prompt: str = "Enter folder path") -> str:
    """Prompts the user for a directory path and validates it."""
    while True:
        path = input(f"  {prompt}: ").strip()
        if os.path.isdir(path):
            return path
        print(f"  ⚠  '{path}' is not a valid directory. Please try again.\n")


def feature_organise() -> None:
    """Interactive handler for Feature 1: Organise Files."""
    print("\n─── Organise Files by Type ───\n")
    source = get_directory("Enter the folder to organise")
    dry    = input("  Preview only? (dry run) [y/N]: ").strip().lower() == "y"
    organize_folder(source, dry_run=dry)


def feature_rename() -> None:
    """Interactive handler for Feature 2: Bulk Rename."""
    print("\n─── Bulk Rename Files ───\n")
    print("  Available strategies:")
    print("    sequential  — file_001.jpg, file_002.jpg …")
    print("    prefix      — adds text before the filename")
    print("    suffix      — adds text before the extension")
    print("    replace     — find & replace text in the filename")
    print("    lowercase   — converts all filenames to lowercase\n")

    source   = get_directory("Enter the folder with files to rename")
    strategy = input("  Choose strategy: ").strip().lower()
    dry      = input("  Preview only? (dry run) [y/N]: ").strip().lower() == "y"

    kwargs = {"source_dir": source, "strategy": strategy, "dry_run": dry}

    if strategy == "sequential":
        kwargs["base_name"] = input("  Base name (default 'file'): ").strip() or "file"
        kwargs["start"]     = int(input("  Start number (default 1): ").strip() or "1")
        kwargs["padding"]   = int(input("  Zero-pad digits (default 3): ").strip() or "3")

    elif strategy == "prefix":
        kwargs["prefix"] = input("  Prefix to add: ").strip()

    elif strategy == "suffix":
        kwargs["suffix"] = input("  Suffix to add (before extension): ").strip()

    elif strategy == "replace":
        kwargs["find"]         = input("  Text to find: ").strip()
        kwargs["replace_with"] = input("  Replace with: ").strip()

    bulk_rename(**kwargs)


def feature_dedup() -> None:
    """Interactive handler for Feature 3: Remove Duplicates."""
    print("\n─── Remove Duplicate Files ───\n")
    source    = get_directory("Enter the folder to scan")
    recursive = input("  Include sub-folders? [Y/n]: ").strip().lower() != "n"
    dry       = input("  Preview only? (dry run) [y/N]: ").strip().lower() == "y"
    remove_duplicates(source, recursive=recursive, dry_run=dry)


def feature_auto_move() -> None:
    """Interactive handler for Feature 4: Auto-Move with Rules."""
    print("\n─── Auto-Move Files by Rules ───\n")
    print("  This demo creates 3 example rules:")
    print("    • .pdf  files → ./PDFs")
    print("    • Files starting with 'invoice' → ./Invoices")
    print("    • Files > 10 MB → ./LargeFiles\n")

    source = get_directory("Enter the source folder")
    dry    = input("  Preview only? (dry run) [y/N]: ").strip().lower() == "y"

    rules = [
        rule_by_extension(".pdf",  os.path.join(source, "PDFs")),
        rule_by_prefix("invoice",  os.path.join(source, "Invoices")),
        rule_by_size_above(10 * 1024 * 1024, os.path.join(source, "LargeFiles")),
    ]
    auto_move(source, rules, dry_run=dry)


def feature_demo() -> None:
    """
    Creates a temporary sample_data folder with dummy files, then runs
    all four features so you can see the toolkit in action immediately.
    """
    import shutil
    import tempfile

    print("\n─── Running Full Demo ───\n")
    demo_dir = os.path.join(os.path.dirname(__file__), "sample_data", "demo_run")
    os.makedirs(demo_dir, exist_ok=True)

    # Create dummy files of various types
    sample_files = [
        "photo1.jpg", "photo2.jpg", "photo_copy.jpg",
        "video_clip.mp4", "document.pdf", "report.docx",
        "notes.txt", "script.py", "archive.zip",
        "music.mp3", "spreadsheet.xlsx",
        "invoice_2024_01.pdf", "invoice_2024_02.pdf",
    ]
    for fname in sample_files:
        fpath = os.path.join(demo_dir, fname)
        with open(fpath, "w") as f:
            f.write(f"Dummy content for {fname}\n")

    # Make two truly identical files so deduplication has something to do
    with open(os.path.join(demo_dir, "photo1.jpg"), "w") as f:
        f.write("identical content")
    with open(os.path.join(demo_dir, "photo_copy.jpg"), "w") as f:
        f.write("identical content")   # Same content → will be detected as duplicate

    print(f"  ✅ Created {len(sample_files)} sample files in '{demo_dir}'\n")

    print("  ── Step 1: Organise by file type (dry run) ──")
    organize_folder(demo_dir, dry_run=True)

    print("  ── Step 2: Bulk rename — sequential (dry run) ──")
    bulk_rename(demo_dir, strategy="sequential", base_name="demo_file", dry_run=True)

    print("  ── Step 3: Find duplicates (dry run) ──")
    remove_duplicates(demo_dir, dry_run=True)

    print("  ── Step 4: Auto-move invoices (dry run) ──")
    rules = [
        rule_by_contains("invoice", os.path.join(demo_dir, "Invoices")),
        rule_by_extension(".py",    os.path.join(demo_dir, "Code")),
    ]
    auto_move(demo_dir, rules, dry_run=True)

    print(f"\n  Demo complete!  Sample files are in: {demo_dir}\n")
    print("  Re-run without dry_run=True to apply changes for real.\n")


# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------
def main() -> None:
    actions = {
        "1": feature_organise,
        "2": feature_rename,
        "3": feature_dedup,
        "4": feature_auto_move,
        "5": feature_demo,
    }

    while True:
        print_menu()
        choice = input("  Your choice: ").strip()

        if choice == "0":
            print("\n  Goodbye! 👋\n")
            sys.exit(0)

        action = actions.get(choice)
        if action:
            try:
                action()
            except KeyboardInterrupt:
                print("\n  Cancelled.\n")
        else:
            print("\n  ⚠  Invalid choice. Please enter 0–5.\n")

        input("  Press Enter to return to the menu …\n")


if __name__ == "__main__":
    main()
