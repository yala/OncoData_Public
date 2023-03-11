"""Script to generate summary statistics for DICOM metadata."""

import argparse
import json
from os.path import dirname, realpath
import sys

sys.path.append(dirname(dirname(dirname(realpath(__file__)))))

from oncodata.dicom_metadata.summarize import summarize


def main(metadata_paths, summary_path):
    """Loads metadata and creates and saves summary statistics.

    Arguments:
        metadata_paths(list): An array of paths to DICOM metadata JSONs.
        summary_path(str): The path where the summary statistics JSON
            will be saved.
    """

    metadata = []
    for metadata_path in metadata_paths:
        with open(metadata_path, "r") as metadata_file:
            metadata.extend(json.load(metadata_file))

    summary = summarize(metadata)

    with open(summary_path, "w") as summary_file:
        json.dump(summary, summary_file, indent=4, sort_keys=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--metadata_paths",
        nargs="+",
        type=str,
        required=True,
        help="List of paths to JSON files containing DICOM metadata.",
    )
    parser.add_argument(
        "--summary_path",
        type=str,
        required=True,
        help="Path to a JSON file where the summary will be saved.",
    )
    args = parser.parse_args()

    main(args.metadata_paths, args.summary_path)
