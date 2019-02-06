import os
from os import listdir
from os.path import isfile, join
import sys
import shutil
mypath = sys.argv[1]

dirs = ["less", "high"]
threshold = 0.3
for dire in dirs:
    if not os.path.exists(dire):
        os.makedirs(dire)
images = [os.path.join(mypath, f) for f in listdir(mypath) if isfile(join(mypath, f))]
for image in images:
    size = os.stat(image).st_size*1.0/(1024*1024)

    if size > threshold:
       shutil.copy(image, "high") 
    else:
       shutil.copy(image, "less")    

