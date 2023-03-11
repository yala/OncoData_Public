"""Methods used to generate summary statistics for DICOM metadata."""

from collections import Counter


def get_count(dicom_metadata, key):
    """Creates a mapping from values to counts for a DICOM metadata key.

    Arguments:
        dicom_metadata(list): An array of DICOM metadata.
        key(str): A key into the DICOM metadata dictionary.
            Values of this key will be counted.
    Returns:
        A dictionary mapping values to the number of DICOMs
        with that value.
    """

    values = [row.get(key, "None") for row in dicom_metadata]
    counts = Counter(values)

    return dict(counts)


def get_num_dicoms_to_count(dicom_metadata):
    """Creates a mapping from number of DICOMs to number of accessions containing that many DICOMs.

    Arguments:
        dicom_metadata(list): An array of DICOM metadata.
    Returns:
        A dictionary mapping number of DICOMs to the number
        of accessions containing that many DICOMs.
    """

    accession_to_num_dicoms = get_count(dicom_metadata, "AccessionNumber")
    accession_to_num_dicoms.pop("None", None)  # Ignore DICOMs with no AccessionNumber
    dicom_counts = accession_to_num_dicoms.values()
    num_dicoms_to_count = Counter(dicom_counts)

    return dict(num_dicoms_to_count)


def get_years(dicom_metadata):
    """Creates a mapping from years to number of DICOMs.

    Arguments:
        dicom_metadata(list): An array of DICOM metadata.
    Returns:
        A dictionary mapping year or "None" to the
        number of DICOMs from that year.
    """

    years = [
        row["StudyDate"][:4] if row.get("StudyDate", None) else "None"
        for row in dicom_metadata
    ]
    year_counts = Counter(years)

    return dict(year_counts)


def summarize(metadata):
    """Generates summary statistics for DICOM metadata.

    Arguments:
        metadata(list): An array of metadata containing
            DICOM metadata.
    Returns:
        A dictionary of summary statistics containing:
        'years': A dictionary mapping year to number of
            DICOMs from that year.
        'num_dicoms_to_count': A dictionary mapping n,
            the number of DICOMs, to the number of accessions
            which contain n DICOMs.
    """

    dicom_metadata = [row["dicom_metadata"] for row in metadata]

    summary = {
        "num_dicoms_to_count": get_num_dicoms_to_count(dicom_metadata),
        "pixel_intensity_relationships": get_count(
            dicom_metadata, "PixelIntensityRelationship"
        ),
        "years": get_years(dicom_metadata),
        "sop_class_uids": get_count(dicom_metadata, "SOPClassUID"),
        "modality": get_count(dicom_metadata, "Modality"),
        "study_description": get_count(dicom_metadata, "StudyDescription"),
    }

    return summary
