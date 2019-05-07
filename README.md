# OncoData
This repo contains data preprocessing scripts for the mammo project.

## Requirements
Required python pip packages are listed in `requirements.txt`. All required pip packages and command line tools can be installed by running `./requirements.sh`.

## DICOM to PNG conversion
DICOMs can be converted to PNGs using the script `dicom_to_png.py` located in the `scripts/dicom_to_png` folder. Conversion can use either the [dcmj2pnm](support.dcmtk.org/docs/dcmj2pnm.html) tool from the [dcmtk](http://dicom.offis.de/dcmtk.php.en) package or the Matlab [dicomread](https://www.mathworks.com/help/images/ref/dicomread.html) tool.

## DICOM metadata extraction
DICOM header metadata can be extracted and saved either as a JSON file or to a SQL table. Both scripts are located in the `scripts/dicom_metadata` folder. To save as a JSON file, use `dicom_metadata_to_json.py`. To save to a SQL table, use `dicom_metadata_to_sql.py`. To examine dicom metadata in the SQL table, use `dicom_metadata_from_sql.py` and replace the query with your own query. DICOM metadata in JSON format can be summarized and plotted using `plot.py` and `summarize.py`.

## Parallel directory copying
A directory can be copied in parallel using `copy_dir_parallel.py` in the `scripts/utils` folder.
