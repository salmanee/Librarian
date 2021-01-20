#!/bin/bash

#script to extract features vectors from ELF binaires

FILES=scripts/Feature_Extractor/extracted_bins.txt
foldername=UnknownLibs_bins
foldername2=UnknownLibs_FVs

echo --- Start Feature Vectors Extraction for binaries listed in $(basename $FILES)---
for file in $(cat $FILES);
do
	echo Extracting features from $file ...
	python3 scripts/Feature_Extractor/extract_feature_vector.py -i $foldername/$file -o $foldername2/$(basename $file .so).json
done
echo --- End of Features Extraction ---
echo All features vectors are stored in JSON files under $foldername2
