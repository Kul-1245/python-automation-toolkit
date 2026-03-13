# 🗂️ Python Automation Toolkit

> A beginner-friendly yet production-quality Python project that automates the most common file management tasks — so you spend less time organising files and more time doing what matters.

---

## 📋 Table of Contents

- [Project Description](#-project-description)
- [Features](#-features)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Usage](#-usage)
  - [Interactive Menu](#interactive-menu)
  - [Programmatic API](#programmatic-api)
- [Example Output](#-example-output)
- [Configuration](#-configuration)
- [Running Tests](#-running-tests)
- [Contributing](#-contributing)
- [License](#-license)

---

## 📖 Project Description

**Python Automation Toolkit** is a modular command-line application that automates four everyday file management tasks:

| # | Feature | What it does |
|---|---------|-------------|
| 1 | **Organise by Type** | Sorts files into sub-folders (`Images/`, `Videos/`, `Documents/`, etc.) based on their extension |
| 2 | **Bulk Rename** | Renames multiple files at once using flexible strategies (sequential, prefix, suffix, find-replace, lowercase) |
| 3 | **Remove Duplicates** | Detects and removes identical files using MD5/SHA-256 hashing — zero false positives |
| 4 | **Auto-Move by Rules** | Moves files to target folders automatically based on extension, filename pattern, or file size |

Every feature supports a **dry-run mode** — preview exactly what will happen before any file is touched.

---

## ✨ Features

- ✅ **Dry-run mode** on every feature — see changes before they happen
- ✅ **Safe move** — never silently overwrites files; auto-appends `(2)`, `(3)` etc.
- ✅ **Content-based deduplication** — hash comparison, not just filename
- ✅ **Flexible rename strategies** — 5 different strategies to suit any workflow
- ✅ **Rule-based file routing** — match by extension, prefix, suffix, substring, or size
- ✅ **Full logging** — every action is logged to both console and `logs/toolkit.log`
- ✅ **Zero external dependencies** — runs on Python 3.10+ standard library only
- ✅ **Clean modular architecture** — easy to extend with new features

---

## 📁 Project Structure

```
python_automation_toolkit/
│
├── main.py                  # Entry point — interactive menu
├── requirements.txt         # Dependencies (all optional)
│
├── config/
│   ├── __init__.py
│   └── settings.py          # All configuration: categories, hashing, logging
│
├── toolkit/
│   ├── __init__.py
│   ├── organizer.py         # Feature 1: Organise by file type
│   ├── renamer.py           # Feature 2: Bulk rename files
│   ├── deduplicator.py      # Feature 3: Remove duplicates
│   └── mover.py             # Feature 4: Auto-move by rules
│
├── utils/
│   ├── __init__.py
│   ├── file_utils.py        # Shared helpers: hashing, safe-move, listing
│   └── logger.py            # Centralised logging setup
│
├── logs/
│   └── toolkit.log          # Auto-created on first run
│
└── sample_data/             # Auto-created by the demo feature
```

---

## ⚙️ Installation

### Prerequisites

- **Python 3.10 or higher** ([download](https://www.python.org/downloads/))
- No internet connection required — the core toolkit uses only the standard library

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/yourname/python-automation-toolkit.git
cd python-automation-toolkit

# 2. (Optional) Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows

# 3. (Optional) Install optional dependencies
pip install -r requirements.txt
```

That's it — no build step, no database, no configuration required to get started.

---

## 🚀 Usage

### Interactive Menu

Run `main.py` to launch the interactive menu:

```bash
python main.py
```

You'll see:

```
  What would you like to do?

  [1]  Organise files by type  (Images, Videos, Documents …)
  [2]  Bulk rename files
  [3]  Remove duplicate files
  [4]  Auto-move files by rules
  [5]  Run demo  (creates sample files & runs all features)
  [0]  Exit
```

**Tip:** Choose **option 5** first to run the built-in demo — it creates sample files and shows all four features in dry-run mode with no risk to your real files.

---

### Programmatic API

You can also import and call each feature directly in your own scripts:

#### Feature 1 — Organise by type

```python
from toolkit.organizer import organize_folder

# Dry-run first to preview
organize_folder("/path/to/Downloads", dry_run=True)

# Then run for real
organize_folder("/path/to/Downloads")
```

#### Feature 2 — Bulk rename

```python
from toolkit.renamer import bulk_rename

# Sequential: report_001.pdf, report_002.pdf …
bulk_rename("/path/to/folder", strategy="sequential", base_name="report", padding=3)

# Find & replace
bulk_rename("/path/to/folder", strategy="replace", find="IMG_", replace_with="photo_")

# Add a prefix
bulk_rename("/path/to/folder", strategy="prefix", prefix="2024_")
```

#### Feature 3 — Remove duplicates

```python
from toolkit.deduplicator import remove_duplicates, find_duplicates

# Just find them (no deletion)
dupes = find_duplicates("/path/to/folder", recursive=True)

# Find and delete (dry run first!)
remove_duplicates("/path/to/folder", dry_run=True)
remove_duplicates("/path/to/folder")
```

#### Feature 4 — Auto-move by rules

```python
from toolkit.mover import auto_move, rule_by_extension, rule_by_prefix, rule_by_size_above

rules = [
    rule_by_extension(".pdf",  "/Users/me/Documents/PDFs"),
    rule_by_prefix("invoice",  "/Users/me/Documents/Invoices"),
    rule_by_size_above(50 * 1024 * 1024, "/Users/me/LargeFiles"),  # > 50 MB
]

auto_move("/Users/me/Downloads", rules, dry_run=True)
```

---

## 📊 Example Output

### Organise by Type

```
=======================================================
  Organisation Summary
=======================================================
  📁 Audio                  2 file(s)
  📁 Code                   3 file(s)
  📁 Documents              4 file(s)
  📁 Images                 6 file(s)
  📁 Videos                 1 file(s)
-------------------------------------------------------
  Total                    16 file(s)
=======================================================
```

### Bulk Rename (sequential)

```
=================================================================
  Rename Summary  (5 file(s))
=================================================================
  Original Name                   →  New Name
-----------------------------------------------------------------
  IMG_3047.jpg                    →  photo_001.jpg
  IMG_3048.jpg                    →  photo_002.jpg
  IMG_3049.jpg                    →  photo_003.jpg
  screenshot_2024.png             →  photo_004.png
  scan0001.pdf                    →  photo_005.pdf
=================================================================
```

### Remove Duplicates

```
============================================================
  Deduplication Summary
============================================================
  Duplicate groups found :  2
  Files removed          :  3
  Space reclaimed        :  47.2 MB
============================================================
```

### Auto-Move by Rules

```
=================================================================
  Auto-Move Summary
=================================================================
  📁 /Users/me/Documents/PDFs
       • contract.pdf
       • invoice_jan.pdf
  📁 /Users/me/Documents/Invoices
       • invoice_feb.pdf
       • invoice_mar.pdf

  Total moved: 4 file(s)
=================================================================
```

---

## 🔧 Configuration

All settings live in `config/settings.py`. Key options:

| Setting | Default | Description |
|---------|---------|-------------|
| `FILE_CATEGORIES` | See file | Maps category names to file extensions |
| `MISC_FOLDER` | `"Miscellaneous"` | Folder for unrecognised extensions |
| `HASH_ALGORITHM` | `"md5"` | Hash algorithm for duplicate detection |
| `HASH_CHUNK_SIZE` | `8192` | Bytes read per chunk when hashing |
| `LOG_DIR` | `"logs"` | Directory for log files |

---

## 🧪 Running Tests

```bash
pip install pytest
pytest tests/ -v
```

---

## 🤝 Contributing

Pull requests are welcome! To add a new feature:

1. Create a new module in `toolkit/`
2. Export it from `toolkit/__init__.py`
3. Add a menu option in `main.py`
4. Write tests in `tests/`

---

## 📄 License

MIT License — free to use, modify, and distribute.
