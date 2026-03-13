# =============================================================================
# config/settings.py
# Central configuration for the Python Automation Toolkit.
# Modify these settings to customize how the toolkit behaves.
# =============================================================================

# ---------------------------------------------------------------------------
# FILE CATEGORY DEFINITIONS
# Maps category folder names to the file extensions they should contain.
# Add or remove extensions to match your needs.
# ---------------------------------------------------------------------------
FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".tiff", ".ico"],
    "Videos": [".mp4", ".avi", ".mov", ".mkv", ".wmv", ".flv", ".webm", ".m4v"],
    "Audio":  [".mp3", ".wav", ".aac", ".flac", ".ogg", ".wma", ".m4a"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".odt", ".rtf", ".md"],
    "Spreadsheets": [".xls", ".xlsx", ".csv", ".ods"],
    "Presentations": [".ppt", ".pptx", ".odp"],
    "Archives": [".zip", ".tar", ".gz", ".rar", ".7z", ".bz2"],
    "Code": [".py", ".js", ".ts", ".html", ".css", ".java", ".cpp", ".c", ".sh", ".json", ".xml", ".yaml", ".yml"],
    "Executables": [".exe", ".msi", ".dmg", ".pkg", ".deb", ".rpm"],
}

# Folder name for files that don't match any category above
MISC_FOLDER = "Miscellaneous"

# ---------------------------------------------------------------------------
# DUPLICATE FILE DETECTION
# Algorithm used to compare files: 'md5' or 'sha256'
# MD5 is faster; SHA256 is more collision-resistant.
# ---------------------------------------------------------------------------
HASH_ALGORITHM = "md5"

# Chunk size (in bytes) for reading large files during hashing.
# 8192 bytes (8 KB) is a safe default that works on all systems.
HASH_CHUNK_SIZE = 8192

# ---------------------------------------------------------------------------
# LOGGING
# ---------------------------------------------------------------------------
LOG_DIR = "logs"
LOG_FILE = "toolkit.log"
LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
