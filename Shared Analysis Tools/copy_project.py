#!/usr/bin/env python3
"""Copy an Android Gradle project into the MOBISEC_Challenge structure,
excluding build outputs, gradle caches, and (for the FileHasher project only)
the huge bundled tools/ directory."""
import shutil
import sys
import os

EXCLUDE_DIRS = {'.gradle', 'build', '.idea', 'tools', '.temp', '__pycache__', '.knownPackages'}
EXCLUDE_FILES = {'.knownPackages'}

def copy_project(src, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)

    def ignore(dir_path, names):
        return [n for n in names if n in EXCLUDE_DIRS or n in EXCLUDE_FILES]

    shutil.copytree(src, dest, ignore=ignore)
    print(f"OK: {src} -> {dest}")

if __name__ == '__main__':
    copy_project(sys.argv[1], sys.argv[2])
