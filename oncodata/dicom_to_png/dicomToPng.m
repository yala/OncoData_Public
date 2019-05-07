function dicomToPng( dicomsFilePath, pngsFilePath )
%Converts DICOM files to 16-bit PNG images.
    % dicomsFilePath(str): The name of a text file containing DICOM paths.
    % pngsFilePath(str): The name of a text file containing PNG paths.
    % run from command line with:
    % matlab -nodisplay -nodesktop -nojvm -r "dicomToPng('dicom_paths.txt', 'png_paths.txt')"

    dicomsFile = fopen(dicomsFilePath, 'r');
    dicomPaths = textscan(dicomsFile, '%s');
    dicomPaths = dicomPaths{1};

    pngsFile = fopen(pngsFilePath, 'r');
    pngPaths = textscan(pngsFile, '%s');
    pngPaths = pngPaths{1};

    numDicoms = length(dicomPaths);

    parfor i = 1:numDicoms
        dicomPath = dicomPaths{i};
        pngPath = pngPaths{i};

        try
            image = dicomread(dicomPath);
            image_double = double(image);
            image_maximum = max(image_double(:));
            image_scaled = image_double / image_maximum;
            imwrite(image_scaled, pngPath, 'BitDepth', 16);
        catch ME
            getReport(ME)
        end
    end
end
