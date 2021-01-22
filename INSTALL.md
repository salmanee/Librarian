
# Librarian Installation Guide #

## Download Librarian Sources: ##
Before getting started, please make sure Docker is installed and running. You can type ```systemctl status docker``` to check the running status of Docker daemon.

Next, run the following command to clone Librarian:
```
# Using SSH
git clone https://github.com/salmanee/Librarian.git

# Using HTTPS
git clone git@github.com:salmanee/Librarian.git
```
In the **parent** directory of Librarian, run the following command to start docker (which contains a working environment with all requirements installed):
```
docker run --rm -it -v $PWD:/home yhuai/librarian
```
Note that Docker only contains the environment, and the `-v` argument will mount your local copy of Librarian into the container.

If successful, you will see the following message at the bottom of your screen:
```
[root@44c29e2ea5d4 home]# ls
Librarian
```

## Using Librarian: ##

All Librarian scripts are found under `scripts/`:
1. To Extract binaries from the apps in `sample_apps/` to `UnknownLibs_bins`, run the following command:
``` 
python3 cluster_libs.py
```

*Note*: To extract binaries from a new set or larger set of apps, modify *apps_dir* and *dest_folder* in `cluster_libs.py` accordingly. Then make sure that your apps are arranged in a way similar to the structure in `sample_apps/`:
        
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
   
2. To extract the features vector from one binary, run:
```
python3 scripts/Feature_Extractor/extract_feature_vector.py -i <lib.so> -o <out.json>
```
3. To extract the features vectors from a set of binaries:

   3.1. Modify `extracted_bins.txt` to include the binaries you are interested in.
   
   3.2. Update the input and output folders in `run_extract_fv.sh`.
   
   3.3. Then run the following command: 
``` 
./scripts/Feature_Extractor/run_extract_fv.sh 
```
4. To compute the similarity score between two feature vectors, run the following command:
```
python3 scripts/Bin2Bin_Score_Calculator/binsimScore.py -f <file1.json> -f <file2.json>
```

Note that, the script currently showed binaries that matched with a similiarty score of 0.85 and higher.
If ther similiarty sore is less than 0.85, noothing will be displayeed. you an adjust this threshold in the [script](https://github.com/salmanee/Librarian/blob/master/scripts/Bin2Bin_Score_Calculator/binsimScore.py#L75). 

5. To compute the similarity between a set of feature vectors:

   5.1. Modify both `source_bin_FVS.txt` and `extracted_bin_FVS.txt` to include the binaries you are interested in comparing.
   
   5.2. Then run:
   
```
./scripts/Bin2Bin_Score_Calculator/run_bin_sim.sh
```

Examples of what the output looks like when running each of the above commands are provided [here](https://github.com/salmanee/Librarian/tree/master/output_examples).
