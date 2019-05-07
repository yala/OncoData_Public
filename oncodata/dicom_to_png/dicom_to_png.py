"""Functions to confirm DICOM image correctness and then convert DICOMs to 16-bit PNGs using either dcmtk or Matlab."""

import os
from subprocess import Popen
from tempfile import NamedTemporaryFile
import dicom

import numpy as np
from p_tqdm import p_map, p_umap

from oncodata.dicom_to_png.get_slice_count import get_slice_count


def has_one_slice(dicom_path):
    '''Checks if dicom has one splice.

    Arguments:
        dicom_path(str): The path to a dicom files.

    Returns:
        True if mammogram has one slice, false otherwise.
    '''
    try:
        if get_slice_count(dicom_path) != 1:
            print('Mammogram must only have one slice.')
            return False
    except Exception as e:
        print(e)
        return False

    return True


def is_selected_dicom(dicom_path, selection_criteria):
    '''Checks if dicom fits the selection criteria.

    Arguments:
        dicom_path(str): The path to a dicom files.
        selection_criteria (set): set of dictionaries where each dictionary describes a set of key:value selection criteria.

    Returns:
        True if dicom meets the selection criteria of at least one set of selection criteria. If no selection criteria
        is provided, returns true for all readable dicoms.
    '''

    try:
        dicom_data = dicom.read_file(dicom_path)
    except Exception as e:
        print(e)
        return False

    # If no selection criteria provided, return True for any readable dicom
    if len(selection_criteria) == 0: return True
    for criteria in selection_criteria:
        match = True
        for key in criteria.keys():
            target_val = criteria[key]
            dicom_val = str(dicom_data.get(key, None))
            if dicom_val != target_val:
                print('{} wrong type. Got "{}" instead of "{}".'.format(key, dicom_val, target_val))
                match = False
        if match:
            return True

    return False


def create_directory_if_necessary(path):
    """Creates a directory for the given path if necessary.

    Arguments:
        path(str): A file path.
    """

    directory = os.path.dirname(path)

    # exist_ok is only available in python3. Without it, there could be a race condition
    # between the workers to create the directory.
    os.makedirs(directory, exist_ok=True)
    return


def dicom_to_png_dcmtk(dicom_path, image_path, selection_criteria, skip_existing=True):
    """Converts a dicom image to a grayscale 16-bit png image using dcmtk.

    Arguments:
        dicom_path(str): The path to the dicom file.
        image_path(str): The path where the image will be saved.
        selection_criteria (list or tuple): list or tuple of dictionaries where each dictionary describes a set of key:value selection criteria.
        skip_existing(bool): True to skip images which already exist.
    """

    if skip_existing and os.path.exists(image_path):
        return

    # Ensure dicom  fits the selection criteria and only has one slice
    if not (is_selected_dicom(dicom_path, selection_criteria) and has_one_slice(dicom_path)):
        return

    # Create directory for image if necessary
    create_directory_if_necessary(image_path)

    # Convert DICOM to PNG using dcmj2pnm (support.dcmtk.org/docs/dcmj2pnm.html)
    # from dcmtk library (dicom.offis.de/dcmtk.php.en)
    Popen(['dcmj2pnm', '+on2', '--min-max-window', dicom_path, image_path]).wait()


def dicom_to_png_imagemagick(dicom_path, image_path, selection_criteria, skip_existing=True):
    """Converts a dicom image to a grayscale 16-bit png image using ImageMagick.

    Arguments:
        dicom_path(str): The path to the dicom file.
        image_path(str): The path where the image will be saved.
        selection_criteria (list or tuple): list or tuple of dictionaries where each dictionary describes a set of key:value selection criteria.
        skip_existing(bool): True to skip images which already exist.
    """

    if skip_existing and os.path.exists(image_path):
        return

    # Ensure dicom meets selection criteria and only has one slice
    if not (is_selected_dicom(dicom_path, selection_criteria) and has_one_slice(dicom_path)):
        return
    # Create directory for image if necessary
    create_directory_if_necessary(image_path)

    # Convert DICOM to PNG using ImageMagick
    Popen(['convert', dicom_path, image_path]).wait()


def dicom_to_png_matlab(dicom_paths, image_paths, selection_criteria, skip_existing=True):
    """Converts a dicom image to a grayscale 16-bit png image using matlab.

    NOTE: Must be run from oncodata/dicom_to_png directory so that Matlab
    can find the dicomToPng.m conversion script.

    Arguments:
        dicom_paths(list[str]): A list of paths to dicom files.
        image_paths(list[str]): A list of paths where the images will be saved.
        skip_existing(bool): True to skip images which already exist.
    """

    if len(dicom_paths) != len(image_paths):
        print('Error: DICOM paths and image paths must be the same length.')
        exit()

    dicom_paths = np.array(dicom_paths)
    image_paths = np.array(image_paths)

    if skip_existing:
        print('Checking for existing images')
        keep = p_map(lambda image_path: not os.path.exists(image_path), image_paths)
        keep_indices = np.where(keep)
        dicom_paths = dicom_paths[keep_indices]
        image_paths = image_paths[keep_indices]

    # Ensure that dicoms meet selection criteria and only have one slice
    print('Checking for invalid dicoms')
    keep = p_map(lambda dicom_path: is_selected_dicom(dicom_path, selection_criteria) and has_one_slice(dicom_path),
                 dicom_paths)
    keep_indices = np.where(keep)
    dicom_paths = dicom_paths[keep_indices]
    image_paths = image_paths[keep_indices]

    if len(dicom_paths) == 0:
        return

    # Create directory for images if necessary
    print('Creating directories for images')
    p_umap(create_directory_if_necessary, image_paths)

    # Save paths to temporary files which will be loaded by matlab
    with NamedTemporaryFile(suffix='.txt') as dicoms_file:
        with NamedTemporaryFile(suffix='.txt') as images_file:
            np.savetxt(dicoms_file.name, dicom_paths, fmt='%s')
            np.savetxt(images_file.name, image_paths, fmt='%s')

            # Convert DICOM to PNG using matlab
            print('Converting with matlab')
            Popen(['matlab', '-nodisplay', '-nodesktop', '-nojvm', '-r',
                   "dicomToPng('%s', '%s'); exit;" % (dicoms_file.name, images_file.name)]).wait()
