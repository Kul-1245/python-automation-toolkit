# =============================================================================
# toolkit/organizer.py
# Feature 1: Organize Files by Type
#
# Scans a folder and moves every file into a sub-folder that matches its
# type (Images, Videos, Documents, etc.) as defined in config/settings.py.
# Files with unrecognised extensions go into a "Miscellaneous" folder.
# =============================================================================

import os
from pathlib import Path

from config.settings import FILE_CATEGORIES, MISC_FOLDER
from utils.file_utils import list_files, safe_move
from utils.logger import get_logger

logger = get_logger("organizer")


def get_category(extension: str) -> str:
    """
    Maps a file extension to its human-readable category name.

    Args:
        extension: The file extension including the dot, e.g. '.jpg'.

    Returns:
        Category name string, e.g. 'Images', or MISC_FOLDER if unknown.
    """
    ext_lower = extension.lower()
    for category, extensions in FILE_CATEGORIES.items():
        if ext_lower in extensions:
            return category
    return MISC_FOLDER


def organize_folder(source_dir: str, dry_run: bool = False) -> dict:
    """
    Organises all files in source_dir by moving them into category sub-folders.

    Args:
        source_dir: Path to the folder you want to organise.
        dry_run:    If True, prints what WOULD happen without moving anything.
                    Great for previewing before committing changes.

    Returns:
        A summary dict: { category_name: [list_of_moved_files] }
    """
    logger.info(f"{'[DRY RUN] ' if dry_run else ''}Organising folder: '{source_dir}'")

    files = list_files(source_dir, recursive=False)
    if not files:
        logger.warning(f"No files found in '{source_dir}'.")
        return {}

    summary: dict[str, list] = {}

    for filepath in files:
        path_obj = Path(filepath)
        extension = path_obj.suffix          # e.g. '.png'
        category  = get_category(extension)  # e.g. 'Images'
        dest_dir  = os.path.join(source_dir, category)

        # Track results per category
        summary.setdefault(category, [])

        if dry_run:
            logger.info(f"  [WOULD MOVE] '{path_obj.name}' → '{category}/'")
            summary[category].append(path_obj.name)
        else:
            result = safe_move(filepath, dest_dir)
            if result:
                logger.info(f"  Moved '{path_obj.name}' → '{category}/'")
                summary[category].append(path_obj.name)

    # Print a tidy summary table
    _print_summary(summary, dry_run)
    return summary


def _print_summary(summary: dict, dry_run: bool) -> None:
    """Prints a formatted summary of what was (or would be) moved."""
    print("\n" + "=" * 55)
    print(f"  {'DRY RUN — ' if dry_run else ''}Organisation Summary")
    print("=" * 55)
    if not summary:
        print("  Nothing to organise.")
    else:
        total = 0
        for category, files in sorted(summary.items()):
            count = len(files)
            total += count
            print(f"  📁 {category:<20} {count:>4} file(s)")
        print("-" * 55)
        print(f"  {'Total':<20} {total:>4} file(s)")
    print("=" * 55 + "\n")
