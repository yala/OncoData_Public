from os.path import dirname, realpath, join
import sys

sys.path.append(dirname(dirname(realpath(__file__))))
from tempfile import NamedTemporaryFile
import unittest

import numpy as np
from scipy.misc import imread

from oncodata.dicom_to_png.dicom_to_png import dicom_to_png_dcmtk

test_dir = dirname(realpath(__file__))


class DicomToPngTests(unittest.TestCase):
    def test_dicom_to_png_dcmtk(self):
        correct_png = imread(join(test_dir, 'test_data', 'test.png'))
        selection_criteria = []
        dicom_path = join(test_dir, 'test_data', 'test.dcm')
        with NamedTemporaryFile(suffix='.png') as png_file:
            dicom_to_png_dcmtk(dicom_path, png_file.name, selection_criteria, skip_existing=False)
            png = imread(png_file.name)
        self.assertTrue(np.array_equal(correct_png, png))


if __name__ == '__main__':
    unittest.main()
