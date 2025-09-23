import os
import shutil
from pathlib import Path


def copy_files_recursive(source_dir_path: Path|str, dest_dir_path: Path|str):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    for filename in os.listdir(source_dir_path):
        from_path = os.path.join(source_dir_path, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        print(f" * {from_path} -> {dest_path}")
        if os.path.isfile(from_path):
            _=shutil.copy(from_path, dest_path)
        else:
            copy_files_recursive(from_path, dest_path)
