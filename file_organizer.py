import os
import shutil
import argparse
from collections import defaultdict
from pathlib import Path

# Define file extensions.
FILE_TYPE_MAPPINGS = {
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".svg"},
    "Documents": {".pdf", ".docx", ".doc", ".txt", ".pptx", ".xlsx", ".odt", ".rtf", ".csv", ".json"},
    "Videos": {".mp4", ".mov", ".avi", ".mkv", ".wmv"},
    "Audio": {".mp3", ".wav", ".flac", ".aac", ".ogg"},
    "Archives": {".zip", ".tar", ".gz", ".bz2", ".7z", ".rar"},
    "Code": {".py", ".ipynb", ".js", ".ts", ".css", ".html", ".json", ".xml", ".yaml", ".yml", ".md", ".mdx"},
    "Programs": {".exe", ".msi", ".app", ".dmg", ".pkg", ".deb", ".rpm", ".iso"},
    "Others": {"*"}
}

def get_category(file_path):
    """Determines the file category based on its extension."""
    file_extension = Path(file_path).suffix.lower()
    for category, extensions in FILE_TYPE_MAPPINGS.items():
        if file_extension in extensions:
            return category
    return "Others"

def print_summary(moved_files_count):
    """Prints a summary of the file organization operations."""
    print("\n--- Organization Summary ---")
    if not moved_files_count:
        print("No files were found to organize.")
        return

    for category, count in sorted(moved_files_count.items()):
        print(f"- Moved {count} file(s) to {category}/")
    print("\nOrganization complete.")

def organize_files(source_folder, simulate=False):
    """
    Organizes files in a source folder into subdirectories by type.

    Args:
        source_folder (str): The path to the folder to organize.
        simulate (bool): If True, prints planned actions without moving files.
    """
    moved_files_count = defaultdict(int)
    print(f"Scanning folder: {source_folder}\n")

    for filename in os.listdir(source_folder):
        source_path = os.path.join(source_folder, filename)
        if not os.path.isfile(source_path):
            continue

        category = get_category(source_path)
        destination_folder = os.path.join(source_folder, category)

        try:
            if not simulate:
                os.makedirs(destination_folder, exist_ok=True)
                shutil.move(source_path, os.path.join(destination_folder, filename))
                print(f"Moving '{filename}' to '{category}/'")
            else:
                print(f"[SIMULATE] Move '{filename}' to '{category}/'")
            
            moved_files_count[category] += 1
        # Exception handling of non-authorized files.
        except (OSError, PermissionError) as e:
            print(f"[ERROR] Could not move '{filename}': {e}")
        
    print_summary(moved_files_count)


def main():
    parser = argparse.ArgumentParser(description="Organize files in a folder by their type.")
    parser.add_argument(
        "folder_path", 
        nargs='?', 
        default=None, 
        help="The path to the folder to organize. If not provided, you will be prompted."
    )
    parser.add_argument(
        "--simulate", 
        action="store_true", 
        help="Run the script in simulation mode; no files will be moved."
    )
    args = parser.parse_args()

    # Get the folder path from arguments or user input.
    target_folder = args.folder_path
    if not target_folder:
        target_folder = input("Enter the path to the folder you want to organize: ")

    # Validate the provided path.
    if not os.path.isdir(target_folder):
        print(f"Error: The path '{target_folder}' is not a valid directory.")
        return

    organize_files(target_folder, args.simulate)

if __name__ == "__main__":
    main()