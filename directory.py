import os
import shutil


def create_dir(path):
    os.makedirs(path, exist_ok=True)


def delete_dir(path):
    if os.path.exists(path):
        shutil.rmtree(path)
