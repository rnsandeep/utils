import sys, shutil, os
import random
import string
from file_utils import files_with_ext, create_dir

mypath = sys.argv[1]
newpath = sys.argv[2]

source_text = sys.argv[3]

create_dir(newpath)

jpegfiles = [os.path.join(mypath, s.strip()+'.jpg') for s in open(source_text,'r').readlines()]

copyfiles = jpegfiles
#jpegfiles = files_with_ext(mypath, '.jpg') # get all the files with extentsion

for f in copyfiles:
    dest = os.path.join(newpath, os.path.basename(f))
    if os.path.exists(dest):
       print(newname)
       os.symlink(f, dest)
    else:
       os.symlink(f, dest)
#       shutil.copy(f, dest)
