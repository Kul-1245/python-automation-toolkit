# =============================================================================
# toolkit/deduplicator.py
# Feature 3: Remove Duplicate Files
#
# Scans a folder (optionally recursive) and identifies files with identical
# content using cryptographic hashing.  For each group of duplicates the
# FIRST file found is treated as the "original" and all others are removed
# (or listed, if dry_run=True).
# =============================================================================

import os
from pathlib import Path

from utils.file_utils import hash_file, human_readable_size, list_files
from utils.logger import get_logger

logger = get_logger("deduplicator")


def find_duplicates(source_dir: str, recursive: bool = True) -> dict[str, list[str]]:
    """
    Scans source_dir and groups files that have identical content.

    Args:
        source_dir: The folder to scan.
        recursive:  If True, also scans all sub-folders.

    Returns:
        A dict where each key is a hash and the value is a list of
        file paths that share that hash.  Only groups with 2+ entries
        are returned (i.e. actual duplicates).
    """
    logger.info(f"Scanning for duplicates in '{source_dir}' (recursive={recursive}) …")

    files = list_files(source_dir, recursive=recursive)
    if not files:
        logger.warning(f"No files found in '{source_dir}'.")
        return {}

    hash_map: dict[str, list[str]] = {}

    for filepath in files:
        file_hash = hash_file(filepath)
        if file_hash is None:
            continue  # Unreadable file — skip it
        hash_map.setdefault(file_hash, []).append(filepath)

    # Keep only hashes that have more than one file (the actual duplicates)
    duplicates = {h: paths for h, paths in hash_map.items() if len(paths) > 1}

    logger.info(f"Found {len(duplicates)} duplicate group(s) across {len(files)} file(s).")
    return duplicates


def remove_duplicates(
    source_dir: str,
    recursive: bool = True,
    dry_run: bool = False,
) -> list[str]:
    """
    Finds and removes duplicate files, keeping the first occurrence of each.

    Args:
        source_dir: The folder to scan.
        recursive:  Whether to scan sub-folders.
        dry_run:    If True, prints what WOULD be deleted without deleting.

    Returns:
        List of file paths that were (or would be) removed.
    """
    logger.info(f"{'[DRY RUN] ' if dry_run else ''}Removing duplicates in '{source_dir}'")

    duplicates = find_duplicates(source_dir, recursive=recursive)
    if not duplicates:
        print("\n  ✅ No duplicate files found!\n")
        return []

    removed: list[str] = []
    space_saved: int = 0

    for file_hash, paths in duplicates.items():
        # The first file in the list is the "original" we keep
        original = paths[0]
        copies   = paths[1:]

        logger.info(f"\n  Original  → '{original}'")
        for copy in copies:
            file_size = os.path.getsize(copy)
            space_saved += file_size

            if dry_run:
                logger.info(f"  [WOULD DELETE] '{copy}' ({human_readable_size(file_size)})")
            else:
                try:
                    os.remove(copy)
                    logger.info(f"  Deleted '{copy}' ({human_readable_size(file_size)})")
                    removed.append(copy)
                except OSError as e:
                    logger.error(f"  Could not delete '{copy}': {e}")

            removed.append(copy) if dry_run else None

    _print_dedup_summary(duplicates, removed, space_saved, dry_run)
    return removed


def _print_dedup_summary(
    duplicates: dict,
    removed: list,
    space_saved: int,
    dry_run: bool,
) -> None:
    """Prints a summary of duplicate groups and space reclaimed."""
    print("\n" + "=" * 60)
    print(f"  {'DRY RUN — ' if dry_run else ''}Deduplication Summary")
    print("=" * 60)
    print(f"  Duplicate groups found : {len(duplicates)}")
    print(f"  Files {'to remove' if dry_run else 'removed'}      : {len(removed)}")
    print(f"  Space {'to reclaim' if dry_run else 'reclaimed'}    : {human_readable_size(space_saved)}")
    print("=" * 60 + "\n")
