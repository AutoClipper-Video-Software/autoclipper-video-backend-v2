from pathlib import Path
import os


def delete_files(files: list[Path]):
    for file in files:
        os.remove(file)
