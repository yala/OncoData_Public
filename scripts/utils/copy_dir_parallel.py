"""Copies all files from one directory to another, preserving directory structure"""

import argparse
import os
from shutil import copyfile

from p_tqdm import p_umap


def main(source_dir, dest_dir):
    """Copies all files from one directory to another
    while preserving the underlying directory structure.

    Arguments:
        source_dir(str): The directory with files to copy.
        dest_dir(str): The directory where the files will be copied to.
    """

    paths = []
    for root, _, files in os.walk(source_dir):
        paths.extend([os.path.join(root, f) for f in files])

    def copy(source_path, skip_existing=True):
        """Copies a file from source_path to source_path with
        source_dir replaced by dest_dir.

        Arguments:
            source_path(str): Path to a file to be copied.
            skip_existing(bool): True to skip copying files
                when the destination file already exists.
        """

        dest_path = source_path.replace(source_dir.strip("/"), dest_dir.strip("/"))

        # Skip if dest file already exists
        if skip_existing and os.path.exists(dest_path):
            return

        # Create directory if necessary
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)

        copyfile(source_path, dest_path)

    p_umap(copy, paths)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source_dir", type=str, required=True, help="Source directory"
    )
    parser.add_argument(
        "--dest_dir", type=str, required=True, help="Destination directory"
    )
    args = parser.parse_args()

    main(args.source_dir, args.dest_dir)
