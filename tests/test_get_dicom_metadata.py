from os.path import dirname, realpath
import sys
sys.path.append(dirname(dirname(realpath(__file__))))
from tempfile import NamedTemporaryFile, TemporaryDirectory
import unittest

from oncodata.dicom_metadata.get_dicom_metadata import get_dicom_metadata

DICOM_METADATA = {
    'AccessionNumber': '2',
    'AcquisitionDate': '20061207',
    'AcquisitionNumber': '1',
    'AcquisitionTime': '091414.0157',
    'AdmittingDiagnosesDescription': '',
    'AveragePulseWidth': '4',
    'BitsAllocated': '16',
    'BitsStored': '10',
    'CenterOfCircularShutter': '[512, 512]',
    'ColumnAngulation': '0',
    'Columns': '1024',
    'ContentDate': '20061207',
    'ContentTime': '091414.0157',
    'ContrastBolusAgent': '',
    'CurrentPatientLocation': 'RAD',
    'DeidentificationMethod': "['dcanon', 'no identifiers', 'keep descriptions', 'keep manufacturer', 'keep retired', 'no private', 'no uids', 'no pet demographics', 'keep dates']",
    'DistanceSourceToDetector': '1150',
    'DistanceSourceToPatient': '972',
    'EstimatedRadiographicMagnificationFactor': '1.1831',
    'ExposureTime': '4',
    'FieldOfViewDimensions': '300',
    'FieldOfViewShape': 'ROUND',
    'FilterType': 'CU_0.0_MM',
    'HighBit': '9',
    'ImageAndFluoroscopyAreaDoseProduct': '0.3',
    'ImageType': "['ORIGINAL', 'PRIMARY', 'SINGLE PLANE']",
    'ImagerPixelSpacing': '[0.293, 0.293]',
    'InstanceCreationDate': '20070112',
    'InstanceCreationTime': '093126',
    'InstanceCreatorUID': '1.3.6.1.4.1.5962.3',
    'InstanceNumber': '1',
    'IntensifierSize': '367',
    'KVP': '93',
    'Laterality': '',
    'Manufacturer': 'SIEMENS',
    'ManufacturerModelName': 'FLUOROSPOT_COMPACT',
    'Modality': 'RF',
    'PatientBirthDate': '',
    'PatientID': 'TEST2351267',
    'PatientIdentityRemoved': 'YES',
    'PatientName': 'Test^FluroWithDisplayShutter',
    'PatientOrientation': '',
    'PatientSex': '',
    'PerformedProcedureStepDescription': 'UPPER GI SERIES (STOMACH)',
    'PhotometricInterpretation': 'MONOCHROME2',
    'PixelIntensityRelationship': 'LIN',
    'PixelRepresentation': '0',
    'PixelSpacing': '[0.293, 0.293]',
    'ProcedureCodeSequence': "[(0008, 0100) Code Value                          SH: 'RADUGI'\n(0008, 0102) Coding Scheme Designator            SH: 'BROKER'\n(0008, 0104) Code Meaning                        LO: 'UPPER GI SERIES (STOMACH)']",
    'RadiationMode': 'PULSED',
    'RadiationSetting': 'GR',
    'RadiusOfCircularShutter': '517',
    'ReferringPhysicianName': '',
    'RequestingPhysician': '',
    'Rows': '1024',
    'SOPClassUID': '1.2.840.10008.5.1.4.1.1.12.2',
    'SOPInstanceUID': '1.3.6.1.4.1.5962.1.1.0.0.0.1168612284.20369.0.3',
    'SamplesPerPixel': '1',
    'SeriesDate': '20061207',
    'SeriesDescription': 'Barium        3F/s',
    'SeriesInstanceUID': '1.3.6.1.4.1.5962.1.1.0.0.0.1168612284.20369.0.2',
    'SeriesNumber': '1',
    'SeriesTime': '091414.0157',
    'ShutterLeftVerticalEdge': '233',
    'ShutterLowerHorizontalEdge': '1018',
    'ShutterRightVerticalEdge': '789',
    'ShutterShape': "['RECTANGULAR', 'CIRCULAR']",
    'ShutterUpperHorizontalEdge': '5',
    'SoftwareVersions': 'VE20F',
    'SpecificCharacterSet': 'ISO_IR 100',
    'StudyDate': '20061207',
    'StudyDescription': 'UPPER GI SERIES (STOMACH)',
    'StudyID': '2',
    'StudyInstanceUID': '1.3.6.1.4.1.5962.1.1.0.0.0.1168612284.20369.0.1',
    'StudyTime': '091414',
    'TableAngle': '89',
    'TableMotion': 'STATIC',
    'TimezoneOffsetFromUTC': '-0500',
    'WindowCenter': '640',
    'WindowWidth': '588',
    'XRayTubeCurrent': '325'
}

class GetDicomMetadataTests(unittest.TestCase):
    def test_get_metadata(self):
        correct_metadata = DICOM_METADATA

        metadata = get_dicom_metadata('test_data/test.dcm')

        self.assertDictEqual(correct_metadata, metadata)

if __name__ == '__main__':
    unittest.main()