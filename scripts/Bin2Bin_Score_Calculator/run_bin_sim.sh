#!/bin/bash

#runs binsimScore between a set of FVS

Source_bins=scripts/Bin2Bin_Score_Calculator/source_bin_FVS.txt
Extracted_bins=scripts/Bin2Bin_Score_Calculator/extracted_bin_FVS.txt
Extracted_bins_folder=UnknownLibs_FVs
Source_bins_folder=KnownLibs_FVs

echo --- Calculating the similarity score between binaries listed in $(basename $Extracted_bins) and binariess in $(basename $Source_bins) ---
for file1 in $(cat $Extracted_bins);
do
    for file2 in $(cat $Source_bins):
    do
	python3 scripts/Bin2Bin_Score_Calculator/binsimScore.py -f $Extracted_bins_folder/$file1 -f $Source_bins_folder/$file2
    done
done
echo --- End of Similarity Computations ---

