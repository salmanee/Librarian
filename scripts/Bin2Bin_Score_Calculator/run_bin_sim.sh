#!/bin/bash

#runs binsimScore between a set of FVS

Source_bins=source_bin_FVS.txt
Extracted_bins=extracted_bin_FVS.txt
Extracted_bins_folder=../../UnknownLibs_FVs
Source_bins_folder=../../KnownLibs_FVs

for file1 in $(cat $Extracted_bins);
do
    for file2 in $(cat $Source_bins):
    do
	python3 similarity_single_file.py -f $Extracted_bins_folder/$file1.json -f $Source_bins_folder/$file2 2> /dev/null
    done
done
