#!/bin/bash

#script to extract features vectors from ELF binaires

FILES=extracted_bins.txt
foldername=../UnknownLibs_bins
foldername2=../UnkonwnLibs_Fvs

for file in $(cat $FILES);
do
    python3 extract_feature_vector.py -i $foldername/$file -o $foldername2/$(basename $file .so).json
done
