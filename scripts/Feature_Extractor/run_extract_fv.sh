#!/bin/bash

#script to extract features vectors from ELF binaires

FILES=scripts/Feature_Extractor/extracted_bins.txt
foldername=UnknownLibs_bins
foldername2=UnknownLibs_FVs

for file in $(cat $FILES);
do
    python3 scripts/Feature_Extractor/extract_feature_vector.py -i $foldername/$file -o $foldername2/$(basename $file .so).json
done
