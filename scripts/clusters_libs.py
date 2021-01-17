#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Extracts biniares from apps and clusters them based on their sha256

import os
import subprocess
import json
import hashlib
import shutil
import time

apps_dir="../sample_apps"
dest_folder = "UnKnownLibs_bins"
start_time=time.time()

for app in os.listdir(apps_dir):
    if app.endswith(".apk"):
        # Iterates and unzips each .apk per app
        subprocess.call(["unzip -j -o %s %s -d %s" % (os.path.join(apps_dir,app),"lib/*","temp")],
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
                    renamed_native=binary[:-3]+"_"+app+".so"
                    if(not(os.path.exists(os.path.join(dest_folder,cluster_name)))):
                        os.mkdir(os.path.join(dest_folder,cluster_name))
                    #shutil.move(os.path.join("temp",binary),os.path.join(cluster_name,renamed_native))
        subprocess.call(["rm","-r","temp"])

end_time=time.time()
print("total execution time:{:.2f} sec".format(end_time-start_time))
