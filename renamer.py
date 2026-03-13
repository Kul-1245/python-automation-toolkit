# =============================================================================
# toolkit/renamer.py
# Feature 2: Bulk Rename Files
#
# Renames every file in a folder according to a chosen strategy:
#   - 'sequential' : photo_001.jpg, photo_002.jpg, photo_003.jpg ...
#   - 'prefix'     : adds text before the original name
#   - 'suffix'     : adds text before the extension
#   - 'replace'    : finds and replaces text in the filename
#   - 'lowercase'  : converts all filenames to lowercase
# =============================================================================

import os
from pathlib import Path

from utils.file_utils import list_files
from utils.logger import get_logger

logger = get_logger("renamer")

# The supported rename strategies
STRATEGIES = ("sequential", "prefix", "suffix", "replace", "lowercase")


def bulk_rename(
    source_dir: str,
    strategy: str,
    base_name: str = "file",
    start: int = 1,
    padding: int = 3,
    prefix: str = "",
    suffix: str = "",
    find: str = "",
    replace_with: str = "",
    dry_run: bool = False,
) -> list[tuple[str, str]]:
    """
    Renames files in source_dir according to the chosen strategy.

    Args:
        source_dir:   Folder containing the files to rename.
        strategy:     One of 'sequential', 'prefix', 'suffix', 'replace', 'lowercase'.
        base_name:    Base text used in 'sequential' mode (default 'file').
        start:        Starting counter for 'sequential' mode (default 1).
        padding:      Zero-padding width for the counter, e.g. 3 → 001 (default 3).
        prefix:       Text to prepend in 'prefix' mode.
        suffix:       Text to append (before extension) in 'suffix' mode.
        find:         Text to search for in 'replace' mode.
        replace_with: Text to substitute in 'replace' mode.
        dry_run:      Preview changes without actually renaming.

    Returns:
        List of (old_name, new_name) tuples for every renamed file.
    """
    if strategy not in STRATEGIES:
        logger.error(f"Unknown strategy '{strategy}'. Choose from: {STRATEGIES}")
        return []

    logger.info(f"{'[DRY RUN] ' if dry_run else ''}Bulk rename in '{source_dir}' using strategy='{strategy}'")

    files = list_files(source_dir, recursive=False)
    if not files:
        logger.warning(f"No files found in '{source_dir}'.")
        return []

    renames: list[tuple[str, str]] = []
    counter = start

    for filepath in files:
        path_obj = Path(filepath)
        old_name = path_obj.name
        stem     = path_obj.stem     # filename without extension
        ext      = path_obj.suffix   # extension including the dot

        # Build the new filename based on the chosen strategy
        if strategy == "sequential":
            new_name = f"{base_name}_{str(counter).zfill(padding)}{ext}"
            counter += 1

        elif strategy == "prefix":
            new_name = f"{prefix}{old_name}"

        elif strategy == "suffix":
            new_name = f"{stem}{suffix}{ext}"

        elif strategy == "replace":
            if not find:
                logger.error("'replace' strategy requires a non-empty 'find' argument.")
                return []
            new_name = old_name.replace(find, replace_with)

        elif strategy == "lowercase":
            new_name = old_name.lower()

        # Skip files that wouldn't change
        if new_name == old_name:
            logger.debug(f"  Skipping '{old_name}' (name unchanged).")
            continue

        renames.append((old_name, new_name))

        if dry_run:
            logger.info(f"  [WOULD RENAME] '{old_name}' → '{new_name}'")
        else:
            new_path = path_obj.parent / new_name
            # Guard: don't overwrite an existing file
            if new_path.exists():
                logger.warning(f"  Skipping '{old_name}': '{new_name}' already exists.")
                continue
            os.rename(filepath, str(new_path))
            logger.info(f"  Renamed '{old_name}' → '{new_name}'")

    _print_rename_summary(renames, dry_run)
    return renames


def _print_rename_summary(renames: list, dry_run: bool) -> None:
    """Prints a before/after table of renames."""
    print("\n" + "=" * 65)
    print(f"  {'DRY RUN — ' if dry_run else ''}Rename Summary  ({len(renames)} file(s))")
    print("=" * 65)
    if not renames:
        print("  No files were renamed.")
    else:
        print(f"  {'Original Name':<30}  →  {'New Name'}")
        print("-" * 65)
        for old, new in renames:
            print(f"  {old:<30}  →  {new}")
    print("=" * 65 + "\n")
