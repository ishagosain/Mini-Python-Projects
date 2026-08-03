"""
Smart File Organizer
---------------------
Automatically sorts files in a folder (e.g. Downloads) into
subfolders by category: Images, Documents, Videos, Audio,
Archives, Code, Installers, and Other.
 
Features:
- Dry-run mode to preview changes before moving anything
- Undo support (reverses the last run using a log file)
- Skips files already in category folders
- Uses only the Python standard library
"""

import argparse
import json
import shutil
from pathlib import Path
from datetime import datetime
 
CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".heic"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".xls", ".pptx", ".ppt", ".csv", ".md"],
    "Videos": [".mp4", ".mov", ".avi", ".mkv", ".wmv", ".flv"],
    "Audio": [".mp3", ".wav", ".flac", ".aac", ".m4a"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Code": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".ipynb", ".json", ".sql"],
    "Installers": [".exe", ".msi", ".dmg", ".pkg"],
}
 
LOG_FILENAME = ".file_organizer_log.json"
 
 
def get_category(file_ext):
    for category, extensions in CATEGORIES.items():
        if file_ext.lower() in extensions:
            return category
    return "Other"
 
 
def organize(folder_path, dry_run=False):
    folder = Path(folder_path)
    if not folder.is_dir():
        print(f"Error: '{folder_path}' is not a valid directory.")
        return
 
    category_folders = set(CATEGORIES.keys()) | {"Other"}
    moves = []
 
    for item in folder.iterdir():
        # Skip directories, hidden files, and the log file itself
        if item.is_dir() or item.name.startswith(".") or item.name == LOG_FILENAME:
            continue
        # Skip files that are already sitting inside a category folder
        if item.parent.name in category_folders:
            continue
 
        category = get_category(item.suffix)
        dest_folder = folder / category
        dest_path = dest_folder / item.name
 
        # Avoid overwriting a file with the same name
        counter = 1
        while dest_path.exists():
            dest_path = dest_folder / f"{item.stem}_{counter}{item.suffix}"
            counter += 1
 
        if dry_run:
            print(f"[DRY RUN] Would move: {item.name} -> {category}/")
        else:
            dest_folder.mkdir(exist_ok=True)
            shutil.move(str(item), str(dest_path))
            print(f"Moved: {item.name} -> {category}/")
            moves.append({"original": str(item), "moved_to": str(dest_path)})
 
    if not dry_run and moves:
        log_path = folder / LOG_FILENAME
        log_data = {"timestamp": datetime.now().isoformat(), "moves": moves}
        with open(log_path, "w") as f:
            json.dump(log_data, f, indent=2)
        print(f"\nOrganized {len(moves)} file(s). Run with --undo to reverse this.")
    elif not dry_run:
        print("No files needed organizing.")
 
 
def undo(folder_path):
    folder = Path(folder_path)
    log_path = folder / LOG_FILENAME
 
    if not log_path.exists():
        print("No previous run found to undo.")
        return
 
    with open(log_path, "r") as f:
        log_data = json.load(f)
 
    restored = 0
    for move in log_data["moves"]:
        original = Path(move["original"])
        moved_to = Path(move["moved_to"])
        if moved_to.exists():
            original.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(moved_to), str(original))
            print(f"Restored: {moved_to.name} -> {original.parent.name}/")
            restored += 1
 
    log_path.unlink()
    print(f"\nUndo complete. Restored {restored} file(s).")
 
 
def main():
    parser = argparse.ArgumentParser(description="Organize files in a folder by category.")
    parser.add_argument("path", help="Path to the folder you want to organize")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without moving files")
    parser.add_argument("--undo", action="store_true", help="Undo the last organize run")
    args = parser.parse_args()
 
    if args.undo:
        undo(args.path)
    else:
        organize(args.path, dry_run=args.dry_run)
 
 
if __name__ == "__main__":
    main()
 