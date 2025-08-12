import argparse
import json
import os
import shutil
from collections import defaultdict
from pathlib import Path

# Category -> set of extensions 
DEFAULT_MAP = {
    "Images": {"jpg", "jpeg", "png", "gif", "bmp", "svg", "webp", "tiff"},
    "Documents": {"pdf", "doc", "docx", "txt", "xls", "xlsx", "ppt", "pptx", "odt", "rtf"},
    "Videos": {"mp4", "avi", "mov", "mkv", "webm", "flv"},
    "Audio": {"mp3", "wav", "flac", "aac", "ogg"},
    "Archives": {"zip", "tar", "gz", "bz2", "7z", "rar"},
    "Code": {"py", "js", "ts", "css", "html", "json", "xml", "yaml", "yml", "md", "mdx"},
    "Programs": {"exe", "msi", "app", "dmg", "pkg", "deb", "rpm", "iso"},
    "Others": {"*"}
}