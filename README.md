# File Organizer

A simple yet powerful Python script to automatically organize files in a directory into categorized subfolders based on their file types.

## Features

- **Automatic Categorization**: Sorts files into predefined categories: `Images`, `Documents`, `Videos`, `Audio`, `Archives`, `Code`, `Programs`, and `Others`.
- **Easy to Use**: Run the script from your terminal with a single command.
- **Command-Line Argument**: Specify the target folder directly via a command-line argument.
- **Simulation Mode**: Includes a `--simulate` flag to preview the file organization plan without actually moving any files. This is great for ensuring everything will be organized as expected.
- **Summary Report**: After running, the script prints a clean summary of how many files were moved into each category.
- **Log File**: Automatically generates a `file_organizer_log.txt` to keep a detailed record of all operations, including moved files and errors.

## Demo

<p align="center">
  <video src="assets/Video-demo.mp4" controls="controls" style="max-width: 720px;">
  </video>
</p>

## Installation

**Clone the repository:**

```bash
git clone https://github.com/MohamedMandour10/Organize-Analyze-Manage.git
cd Organize-Analyze-Manage
```

## How to Use

Navigate to the project directory in your terminal and use the following commands.

### Basic Usage

To organize a folder, provide its path as an argument:

```bash
python file_organizer.py "/path/to/your/folder"
```

Replace `"/path/to/your/folder"` with the actual path of the directory you want to clean up.

### Simulation Mode

To see what the script will do without moving any files, use the `--simulate` flag. This is highly recommended for the first run.

```bash
python file_organizer.py "/path/to/your/folder" --simulate
```

### Interactive Mode

If you run the script without providing a path, it will prompt you to enter one:

```bash
python file_organizer.py
```

```
Enter the path to the folder you want to organize: /path/to/your/folder
```
