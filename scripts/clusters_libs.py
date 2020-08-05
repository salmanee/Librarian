#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Extracts biniares from apps and clusters them based on their sha256

import os
import subprocess
import json
import hashlib
import shutil
import time

apps_dir="../downloaded_apks_AndroZoo_May-19-2020"
destination_folder = "../KnownLibs_bins"
start=time.time()

#iterates and unzips each .apk per app
#for each binary under /lib, generate a hash code that corresponds to binary
#create a new directory with binary hash_code (if such folder does not exist), and copy binary to that folder 
for app, root, versions in os.walk(apps_dir):
        for version in versions:
                if version.endswith(".apk"):
                        version_path=os.path.join(app,version)
                        apk_version = version_path[:-4]
                        subprocess.call(["unzip -j -o %s %s -d %s"%(version_path.replace("\"","\\\""), "lib/*",apk_version.replace("\"","\\\""))],shell = True)

                        for file in os.listdir(apk_version):
                                if file.endswith(".so"):
                                        filename = os.path.join(apk_version, file)
                                        with open(filename,"rb") as f:
                                                bytes = f.read() # read entire file as bytes                                                                                                                                                        readable_hash = hashlib.sha256(bytes).hexdigest()
                                        cluster_name=readable_hash
                                        renamed_native=os.path.splitext(file)[0]+"_"+os.path.splitext(version)[0]+".so"
                                        if(not(os.path.exists(cluster_name))):
                                                os.mkdir(cluster_name)
                                        shutil.move(filename,cluster_name+"/"+renamed_native)
                        subprocess.call(["rm","-r",apk_version])
end=time.time()
print("total execution time:{} sec ".format(end-start))
