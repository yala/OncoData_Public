import re
from subprocess import Popen, PIPE
from tempfile import NamedTemporaryFile

import pydicom

def get_slice_count(dicom_path):
    """Determines the number of slices in a DICOM.

    Works by attempting to convert the 1000000th slice
    to a PNG using the command line tool dcmj2pnm. When
    this fails, parses dcmj2pnm's error to determine
    the actual number of slices in the DICOM.

    Arguments:
        dicom_path(str): The path to a dicom.
    Returns:
        The number of slices in the DICOM.
    Raises:
        AttributeError if the output of dcmj2pnm does
        not contain the number of slices in the DICOM.
    """

    with NamedTemporaryFile(suffix='.png') as temp:
        output, err = Popen(['dcmj2pnm', '+on', '+Wi', '1000000', dicom_path, temp.name], stdout=PIPE, stderr=PIPE).communicate()
    err = err.decode('utf-8')
    num_slices = int(re.search(r'only (\d)+ window', err).group(1))

    return num_slices

def get_slice_count_from_metadata(dicom_path):
    """Determines the number of slices in a DICOM.

    Works by reading the DICOM metadata attribute
    at [0x0028, 0x0008], is the number of frames
    in the DICOM. 

    Arguments:
        dicom_path(str): The path to a dicom.
    Returns:
        The number of slices in the DICOM.
    Raises:
        KeyError if the DICOM metadata does not
        contain the NumberOfFrames attribute.
    """

    dicom_data = pydicom.dcmread(dicom_path)
    num_slices = dicom_data[0x0028,0x0008].value

    return num_slices
