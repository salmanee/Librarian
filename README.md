# Librarian:

## Overview: ##
The figure below shows the overall workflow of LibRARIAN. LibRARIAN identifies unknown third-party native libraries and their versions (Unknown Lib Versions) by:
(1) extracting features that distinguish major, minor, and patch versions of libraries that are stable across platforms regardless of underlying architecture or compilation environments 
(2) comparing those features against features from a ground-truth dataset (Known Lib Versions) using a novel similarity metric, bin2sim 
(3) matching against strings that identify version information of libraries extracted from the ground-truth dataset, which we refer to as Version Identification Strings

![Figure 1](/images/approach_cropped.png) 

## Feature Vector Extraction: ##
Our binary similarity detection is based on the extraction of features from binaries combining both metadata found in ELF files as well as identifying features in different binary sections of the library. All shared libraries included in Android apps are compiled into Executable and Linkable Format (ELF) binaries. Like other object files, ELF binaries contain a symbol table with externally visible identifiers such as function names, global symbols, local symbols, and imported symbols.
This symbol table is, on one hand, used during loading and linking and, on the other hand, used by binary analysis tools (e.g., *objdump*, *readelf*, *nm*, *pwntools*, or *angr*) to infer information about the binary.

## Similarity Computation ##
bin2sim is used to determine the similarity between feature vectors. Given two binaries b_1 and b_2 with respective feature vectors FV_1 and FV_2, the bin2sim is the size of the intersection of FV_1 and FV_2 (i.e., the number of common features) over the size of the union of FV_1 and FV_2 (i.e., the number of unique features). The similarity score is a floating-point value between 0 and 1, with a score of 1 indicating identical features, and a score of 0 indicating no shared features between the two libraries.

## Librarian 101 ## 
Librarian's structure in a nutshell:
```
|-- sample_apps
|-- UnknownLibs_bins
|-- UnknownLibs_FVs
|-- knownLibs_FVs
|-- evaluation-results
|-- output_examples
|-- scripts
|   |-- cluster_libs.py
|   |-- Bin2Bin_Score_Calculator
|   |   |-- run_bin_sim.sh
|   |   |-- binsimScore.py
|   |   |-- extracted_bin_FVS.txt
|   |   `-- source_bin_FVS.txt
|   `-- Feature_Extractor
|       |-- run_extract_fv.sh
|       |-- extract_feature_vector.py
|       `-- extracted_bins.txt
```

* sample_apps: Our repository contains the top 200 apps collected from GooglePlay along with their previous releases, obtained from [AndroZoo](https://androzoo.uni.lu/). Due to the large size of this set (209 GB), we provide only 20 unique android packages as a sample with a total of 32 app versions. e.g. *com.instagram.android* has 7 different versions, where the version name is the sha256 of the app version. Naming app versions after their sha256 will enable us later to mtach each app with [version details](https://androzoo.uni.lu/lists) found in AndroZoo such as: vercode, markets, apk_size etc. 
* UnknownLibs_bins: This folder contains biniares extracted from apps in `sample_apps` arranged into folders based on the binary sha256. (Run: `python3 cluster_libs.py` to obtain them). 
For example, cluster/folder `ca8a18f07d0d16e3ce1f4cb35d6d326fd0bbb2a4e82488a937f6feffbfa44b3b` contains 5 identical binaries (share the same sha256), which were extracted from 5 different apps or app versions. 
* UnknownLibs_FVs: Feature vectors extracted from `UnknownLibs_bins` and stored in JSON files.
* KnownLibs_FVs: Features vectors extracted from our groundTruth (KnownLibs) and stored in JSON files.
* scripts:
  * cluster_libs.py: Extracts biniares from the sample_apps folder and clusters them based on their sha256 (to remove duplicates and reduce run time)
  * Feature_Extractor: Scripts needed to extract feature vectors
  * Bin2Bin_Score_Calculator: Scripts needed for computing the similarity score between `knownLibs_FVs` and `UnknownLibs_FVs`  

## Prerequisites: ##
* Python3
* Pre-installation of [angr](https://docs.angr.io/introductory-errata/install)
* Pre-installation of magic:
```
sudo apt-get install python3-magic
```

## Usage: ##
All Librarian scripts are found under `scripts/`:
1. To Extract binaries from the apps in `sample_apps/`, run the following command:
``` 
python3 clusters_libs.py
```
Note: To extract binaries from a new set or larger set apps, follow these steps:
 1.1. Make sure that your apps are arranged in a way similar to the structure in `sample_apps/`:
```
|-- sample_apps
|   |-- app_name_1
|   |   |-- SHA256.apk (app version1)
|   |   |-- SHA256.apk (app version2)
|   |   |-- SHA256.apk (app version3)
|   |   |   ...
|   |   |   ...
|   |   `-- SHA256.apk (app versionX)
|   |-- app_name_2
|   |-- app_name_3
|   |-- app_name_4
|   |-- app_name_5
|   ...
|   ...
|   |
|   `-- app_name_n

```
 1.2. Modify *apps_dir* and *dest_folder* in `clusters_libs.py` accordingly.
 
2. To extract the features vector from one binary, run:
```
scripts/Feature_Extractor/extract_feature_vector.py -i <lib.so> -o <out.json>
```
3. To extract the features vectors from a set of binaries:
 3.1. Modify `extracted_bins.txt` to include the binaries you are intrested in.
 3.2. Update the input and out folders in `run_extract_fv.sh` 
 3.3. Then run the following command: 
``` 
./scripts/Feature_Extractor/run_extract_fv.sh 
```
4. To compute the similarity score between two feature vectors, run the following command:
```
python3 scripts/Bin2Bin_Score_Calculator/binsimScore.py -f <file1.json> -f <file2.json>
```
5. To compute the similarity between a set of feature vectors:
 5.1. modify both `source_bin_FVS.txt` and `extracted_bin_FVS.txt` to include the binaries you are intrested in comparing
 5.2. then run:
```
./scripts/Bin2Bin_Score_Calculator/run_bin_sim.sh
```

Exampples of what the output will look like when running each of the above commands are provided under `output_examples'
## Evaluation Results: ##

