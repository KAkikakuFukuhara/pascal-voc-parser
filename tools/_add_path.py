import sys
import os
from pathlib import Path

def add_package_path():
    this_file_dir_path = Path(os.path.abspath(os.path.dirname(__file__)))
    root_dir_path = str(this_file_dir_path.parent)
    if root_dir_path not in sys.path:
        sys.path.insert(0, root_dir_path)

# call function
add_package_path()
