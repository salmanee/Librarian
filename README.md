# Librarian:

## Overview: ##
LibRARIAN identifies unknown third-party native libraries and their versions (*Unknown Lib Versions*) by (i) extracting features and comparing them against features from a ground truth dataset (*Known Lib Versions*) and (ii) matching identifying “version strings” against common abstracted version information extracted from the ground-truth dataset. The following figure shows the overall workflow of LibRARIAN. 

![Figure 1](/images/approach_cropped-1.png) 

Our binary analysis extracts these features and applies a two-step process. First, the Library Identification phase matches an unknown binary to a library. Second, the Version Identification determines the exact version of the library.


We design a new similarity metric, bin2sim, to identify libraries and their versions. The following figure shows the overall workflow of this similarity metric. 

![Figure 1](/images/bin2bin_cropped-1.png "Figure 2")

LibRARIAN (i) extracts feature vectors from native binaries and (ii) applies bin2sim to generate a similarity score between source and target feature vectors.

## Feature Vector Extraction: ##
Our binary similarity detection is based on the extraction of features from binaries combining both metadata found in ELF files as well as identifying features in different binary sections of the library. All shared libraries included in Android apps are compiled into Executable and Linkable Format (ELF) binaries. Like other object files, ELF binaries contain a symbol table with externally visible identifiers such as function names, global symbols, local symbols, and imported symbols.
This symbol table is, on one hand, used during loading and linking and, on the other hand, used by binary analysis tools (e.g., *objdump*, *readelf*, *nm*, *pwntools*, or *angr*) to infer information about the binary.

## Similarity Computation ##
BinSimScore is used to determine the similarity between feature vectors. Given two binaries b1 and b2 with respective feature vectors FV1 and FV2, the BinSimScore is the size of the intersection of FV1 and FV2 (i.e., the number of common features) over the size of the union of FV1 and FV2 (i.e., the number of unique features). The similarity score is a floating-point value between 0 and 1, with a score of 1 indicating identical features, and a score of 0 indicating no shared features between the two libraries.

## Librarian 101 ## 
Librarian's structure in a nutshell:
```
|-- downloaded_apks_AndroZoo_May-19-2020
|-- KnownLibs_FVs
|-- UnknownLibs_bins
|-- UnknownLibs_FVs
|-- scripts
|   |-- clusters_libs.py
|   |-- Bin2Bin_Score_Calculator
|   |   |-- binsimScore.py
|   |   |-- extracted_bin_FVS.txt
|   |   |-- run_bin_sim.sh
|   |   `-- source_bin_FVS.txt
|   `-- Feature_Extractor
|       |-- extracted_bins.txt
|       |-- extract_feature_vector.py
|       `-- run_extract_fv.sh
```

* downloaded_apks_AndroZoo_May-19-2020: Contains the top 200 apps collected from GooglePlay along with their previous releases (obtained from AndroZoo).
* KnownLibs_FVs: Features vectors extracted from our groundTruth (KnownLibs).
* UnknownLibs_bins: biniares extracted from apps in *downloaded_apks_AndroZoo_May-19-2020* arranged into folders based on their sha256. (Run: `python3 /scripts/cluster_libs.py` to obtain them)
* UnknownLibs_FVs: Features vectors extracted from *UnknownLibs_bins*
* scripts:
  * clusters_libs.py: Extracts biniares from apps and clusters them based on their sha256
  * Feature_Extractor: Scripts needed to extract feature vectors
  * Bin2Bin_Score_Calculator: Scripts needed for computing the similarity score between binaries 

## Prerequisites: ##
* Python3
* Pre-installation of angr (https://docs.angr.io/introductory-errata/install)

## Usage: ##
All Librarian scripts are found under `/scripts/`:
1. To Extract binaries from the apps in /downloaded_apks_AndroZoo_May-19-2020, run the following command:
``` 
python3 clusters_libs.py
```
2. To extract the features vector from one binary, run:
```
python3 extract_feature_vector.py -i <lib.so> -o <out.json>
```
3. To extract the features vectors from a set of binaries, modify `extracted_bins.txt` then run
``` 
./Feature_Extractor/run_extract_fv.sh 
```
4. To compute the similarity score between two feature vectors, run the following command:
```
python3 binsimScore.py -f <file1.json> -f >file2.json>
```
5. To compute the similarity between a set of feature vectors, modify both `source_bin_FVS.txt` and `extracted_bin_FVS.txt` then run:
```
./Bin2Bin_Score_Calculator/run_bin_sim.sh
```

## Access to the entire dataset used in the paper RQs: ##
The following spreedsheet contains an extended version of our evaluation results:
(https://figshare.com/s/f34dde8d3d840df19435)
