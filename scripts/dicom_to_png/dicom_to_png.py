"""Converts DICOM files in a directory to PNG images."""

import argparse
import os
import sys
import pickle

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
)

from p_tqdm import p_umap

from oncodata.dicom_to_png.dicom_to_png import (
    dicom_to_png_dcmtk,
    dicom_to_png_imagemagick,
    dicom_to_png_matlab,
)

MAMMOGRAM_SELECTION_CRITERIA = {
    "SOPClassUID": "Digital Mammography X-Ray Image Storage - For Presentation"
}
BPE_MRI_SELECTION_CRITERIA = {
    "SOPClassUID": "MR Image Storage",
    "SeriesNumber": "2000",
    "InstanceNumber": "8",
}
NO_SELECTION_CRITERIA = {}
DICOM_TYPES = {
    "bpe_mri": BPE_MRI_SELECTION_CRITERIA,
    "mammo": MAMMOGRAM_SELECTION_CRITERIA,
    "generic": NO_SELECTION_CRITERIA,
}


def dicom_path_to_png_path(dicom_path, dicom_dir, png_dir, dicom_ext):
    """Converts a DICOM path to a PNG path by replacing dicom_dir with png_dir in the path.

    Arguments:
        dicom_path(str): Path to a DICOM file.
        dicom_dir(str): Path to a directory containing DICOM files.
        png_dir(str): Path to a directory where PNG version of the
            DICOM images will be saved.
        dicom_ext(str): The extension of the dicom files (should include the dot)

    Returns:
        The same path as dicom_path but with dicom_dir replaced by
        png_dir and with dicom_ext replaced with '.png'.
    """

    dicom_path_after_dir = dicom_path.replace(dicom_dir, "", 1).strip("/")
    png_path_after_dir = dicom_path_after_dir.replace(dicom_ext, "") + ".png"
    png_path = os.path.join(png_dir, png_path_after_dir)

    return png_path


def main(
    dicom_dir,
    dicom_list_pickle_path,
    png_dir,
    dcmtk,
    imagemagick,
    matlab,
    dicom_types,
    dicom_ext,
    window,
):
    """Converts DICOM files in a directory to PNG images.

    NOTE: When using Matlab, must be run from oncodata/dicom_to_png
    directory so that Matlab can find the dicomToPng.m conversion script.

    Arguments:
        dicom_dir(str): Path to a directory containing DICOM files.
        png_dir(str): Path to a directory where PNG versions of the
            DICOM images will be saved.
        dcmtk(bool): True to use dcmtk to convert DICOMs to PNGs.
        imagemagick(bool): True to use ImageMagick to convert DICOMs to PNGs.
        matlab(bool): Ture to use matlab to convert DICOMs to PNGs.
    """
    print("Extracting DICOM paths")
    if dicom_list_pickle_path is not None:
        dicom_paths = pickle.load(open(dicom_list_pickle_path, "rb"))
    else:
        dicom_paths = []
        for root, _, files in os.walk(dicom_dir):
            dicom_paths.extend(
                [
                    os.path.join(root, f)
                    for f in files
                    if (f.endswith(dicom_ext) or dicom_ext == "")
                ]
            )

    image_paths = [
        dicom_path_to_png_path(dicom_path, dicom_dir, png_dir, dicom_ext)
        for dicom_path in dicom_paths
    ]

    selection_criteria = []
    for dicom_type in dicom_types:
        criteria = DICOM_TYPES.get(dicom_type)
        assert (
            criteria is not None
        ), "Unsupported dicom_type. Please add the appropriate type to DICOM_TYPES."
        selection_criteria.append(criteria)
    assert len(selection_criteria) > 0, "No dicoms selected."

    if window:
        selection_criteria = tuple(selection_criteria * len(dicom_paths))
        window = [window] * len(dicom_paths)

    if dcmtk:
        print("Converting to PNG")
        p_umap(dicom_to_png_dcmtk, dicom_paths, image_paths, selection_criteria, window)
    elif imagemagick:
        print("Converting to PNG")
        p_umap(dicom_to_png_imagemagick, dicom_paths, image_paths, selection_criteria)
    elif matlab:
        dicom_to_png_matlab(dicom_paths, image_paths, selection_criteria)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dicom_dir",
        type=str,
        required=True,
        help="Path to a directory containing DICOM files.",
    )
    parser.add_argument(
        "--dicom_list_pickle",
        type=str,
        required=False,
        help="Optionally give a pickle with a list of dicom paths instead of a dicom directory",
    )
    parser.add_argument(
        "--png_dir",
        type=str,
        required=True,
        help="Path to a directory where PNG versions of the DICOM images will be saved.",
    )
    parser.add_argument(
        "--dcmtk",
        default=False,
        action="store_true",
        help="Set flag to use dcmtk to convert DICOMs to PNGs",
    )
    parser.add_argument(
        "--imagemagick",
        default=False,
        action="store_true",
        help="Set flag to use ImageMagick to convert DICOMs to PNGs",
    )
    parser.add_argument(
        "--matlab",
        default=False,
        action="store_true",
        help="Set flag to use matlab to convert DICOMs to PNGs",
    )
    parser.add_argument(
        "--dicom_ext",
        default=".dcm",
        type=str,
        help="The extension of the dicom files. For filtering all other files",
    )
    parser.add_argument(
        "--dicom_types",
        nargs="*",
        default=["bpe_mri", "mammo"],
        help="List of dicom types to convert.",
    )
    parser.add_argument(
        "--window",
        default=False,
        action="store_true",
        help="Set flag to use preset window settings",
    )

    args = parser.parse_args()

    if sum([args.dcmtk, args.imagemagick, args.matlab]) != 1:
        print("Exactly one conversion type must be specified")
        exit()

    if args.dicom_ext == "none":
        args.dicom_ext = ""

    # Create png_dir if it doesn't already exist
    if not os.path.exists(args.png_dir):
        os.makedirs(args.png_dir)

    main(
        args.dicom_dir,
        args.dicom_list_pickle,
        args.png_dir,
        args.dcmtk,
        args.imagemagick,
        args.matlab,
        args.dicom_types,
        args.dicom_ext,
        args.window,
    )
