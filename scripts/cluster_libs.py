#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Sumaya Almanee"
__credits__ = ["Arda Unal", "Mathias Payer" ,"Joshua Garcia"] 
__copyright__ = "Copyright 2021, EPFL and UCI"
__license__ = "GPL"
__version__ = "2.0"

#Extracts biniares from apps and clusters them based on their sha256
import os
import subprocess
import json
import hashlib
import shutil
import time

apps_dir="../sample_apps"
dest_folder = "../UnknownLibs_bins"
start_time=time.time()

print("--- Start Clustering Binaries based on their sha256 ---") 
for app,_,versions in os.walk(apps_dir):
    for version in versions:
        if version.endswith(".apk"):
            # Iterates and unzips each .apk per app
            print("Extracting binaries from {}, version: {} ...".format(os.path.basename(app),version[:-4])) 
            subprocess.call(["unzip -j -o %s %s -d %s" % (os.path.join(apps_dir,app,version),"lib/*","temp")],
                        shell = True,
                        stdout=subprocess.DEVNULL, 
                        stderr=subprocess.STDOUT)

            for binary in os.listdir("temp"):
                if binary.endswith(".so"):
                    with open(os.path.join("temp",binary),"rb") as f:
                        # For each binary under /lib, generate its corresponding hash code
                        bytes = f.read() 
                        cluster_name = hashlib.sha256(bytes).hexdigest()

                        # Create a new directory with binary hash_code (if such folder does not exist), and copy binary to that folder 
                        renamed_native=binary[:-3]+"_"+version[:-4]+".so"
                        cluster_name=os.path.join(dest_folder,cluster_name)
                        if(not(os.path.exists(cluster_name))):
                            os.mkdir(cluster_name)
                        print("Moving binary {} to cluster {}".format(binary[:-3],os.path.basename(cluster_name)))
                        shutil.move(os.path.join("temp",binary),os.path.join(cluster_name,renamed_native))
            subprocess.call(["rm","-r","temp"])
    print("-"*65)

end_time=time.time()

print("--- Total execution time:{:.2f} sec ---".format(end_time-start_time))
