# =============================================================================
# utils/file_utils.py
# Shared helper functions used by multiple toolkit modules.
# Keeps common logic in one place so it isn't repeated everywhere.
# =============================================================================

import hashlib
import os
import shutil
from pathlib import Path
from typing import Optional

from config.settings import HASH_ALGORITHM, HASH_CHUNK_SIZE
from utils.logger import get_logger

logger = get_logger("file_utils")


def hash_file(filepath: str) -> Optional[str]:
    """
    Computes a checksum hash of a file's contents.
    Two files with the same hash are considered identical (duplicates).

    Args:
        filepath: Absolute or relative path to the file.

    Returns:
        A hex-digest string, or None if the file could not be read.
    """
    try:
        hasher = hashlib.new(HASH_ALGORITHM)
        with open(filepath, "rb") as f:
            # Read in chunks to avoid loading huge files into memory at once
            while chunk := f.read(HASH_CHUNK_SIZE):
                hasher.update(chunk)
        return hasher.hexdigest()
    except (OSError, IOError) as e:
        logger.warning(f"Could not hash '{filepath}': {e}")
        return None


def safe_move(src: str, dest_dir: str) -> Optional[str]:
    """
    Moves a file to a destination directory.
    If a file with the same name already exists there, appends a counter
    to the filename to avoid overwriting it — e.g. 'photo(2).jpg'.

    Args:
        src:      Path to the source file.
        dest_dir: Path to the destination directory (will be created if needed).

    Returns:
        The final destination path, or None if the move failed.
    """
    os.makedirs(dest_dir, exist_ok=True)

    src_path = Path(src)
    dest_path = Path(dest_dir) / src_path.name

    # If a file with this name already exists, find a free name
    if dest_path.exists():
        stem = src_path.stem
        suffix = src_path.suffix
        counter = 2
        while dest_path.exists():
            dest_path = Path(dest_dir) / f"{stem}({counter}){suffix}"
            counter += 1

    try:
        shutil.move(str(src_path), str(dest_path))
        logger.debug(f"Moved: '{src_path}' → '{dest_path}'")
        return str(dest_path)
    except (OSError, shutil.Error) as e:
        logger.error(f"Failed to move '{src}' → '{dest_dir}': {e}")
        return None


def list_files(directory: str, recursive: bool = False) -> list[str]:
    """
    Returns a list of all file paths inside a directory.

    Args:
        directory: Path to the folder to scan.
        recursive: If True, also scans all sub-folders.

    Returns:
        A sorted list of absolute file paths (directories are excluded).
    """
    root = Path(directory)
    if not root.is_dir():
        logger.error(f"'{directory}' is not a valid directory.")
        return []

    if recursive:
        # rglob('*') walks every subdirectory
        paths = [str(p) for p in root.rglob("*") if p.is_file()]
    else:
        paths = [str(p) for p in root.iterdir() if p.is_file()]

    return sorted(paths)


def human_readable_size(num_bytes: int) -> str:
    """
    Converts a byte count into a human-readable string like '4.2 MB'.

    Args:
        num_bytes: File size in bytes.

    Returns:
        A formatted string with the appropriate unit.
    """
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if abs(num_bytes) < 1024.0:
            return f"{num_bytes:.1f} {unit}"
        num_bytes /= 1024.0
    return f"{num_bytes:.1f} PB"
