"""Get dicom metadata from all dicoms in a directory and save as a JSON file."""

import argparse
import json
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

from p_tqdm import p_umap

from oncodata.dicom_metadata.get_dicom_metadata import get_dicom_metadata
from oncodata.get_slice_count import get_slice_count

def get_dicom_metadata_and_slice_counts(dicom_path):
    """Gets DICOM metadata and slice counts.

    Argumuments:
        dicom_path(str): Path to a DICOM file.
    Returns:
        A dictionary containing the DICOM path,
        metadata, slice count, and a list of any
        errors encountered while extracting this
        information.
    """
    row = {
        'dicom_path': dicom_path,
        'dicom_metadata': {},
        'slice_count': None,
        'errors': []
    }

    # Get metadata
    try:
        row['dicom_metadata'] = get_dicom_metadata(dicom_path)
    except Exception as e:
        row['errors'].append(str(e))

    # Get slice count
    try:
        row['slice_count'] = get_slice_count(dicom_path)
    except Exception as e:
        row['errors'].append(str(e))

    return row

def main(directory, results_path):
    """Extracts and saves metadata from DICOMs to a JSON file.

    Arguments:
        directory(str): Path to a directory containing DICOMs.
        results_path(str): Path to the JSON where the metadata
            will be saved.
    """

    dicom_paths = []
    for root, _, files in os.walk(directory):
        dicom_paths.extend([os.path.abspath(os.path.join(root, f)) for f in files if f.endswith('.dcm')])
    
    metadata = p_umap(get_dicom_metadata_and_slice_counts, dicom_paths)

    with open(results_path, 'w') as results_file:
        json.dump(metadata, results_file, indent=4, sort_keys=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--directory',
        type=str,
        required=True,
        help='Path to a directory containing DICOMs.')
    parser.add_argument('--results_path',
        type=str,
        required=True,
        help='Path to the JSON where the metadata will be saved.')
    args = parser.parse_args()

    main(args.directory, args.results_path)
