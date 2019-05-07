import dicom

def get_dicom_metadata(dicom_path):
    """Extracts metadata from a dicom file.

    Arguments:
        dicom_path: The path to a dicom file.

    Returns:
        A dictionary containing all the metadata in
        the dicom file besides the image itself.
    Raises:
        InvalidDicomError if the dicom file cannot be read.
    """

    dicom_data = dicom.read_file(dicom_path)
    dicom_keys = dicom_data.dir()
    # Don't add image data to metadata
    if 'PixelData'in dicom_keys:
        dicom_keys.remove('PixelData')
    dicom_metadata = {key: str(dicom_data.get(key)) for key in dicom_keys}

    return dicom_metadata
