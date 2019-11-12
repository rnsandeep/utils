import sys, shutil, os
import random
import string
from file_utils import files_with_ext, create_dir
import pickle

mypath = sys.argv[1]

ages = pickle.load(open(sys.argv[2], "rb"))


#source_text = sys.argv[3]

jpegfiles = files_with_ext(mypath, '.jpg') #[os.path.join(mypath, s.strip()+'.jpg') for s in open(source_text,'r').readlines()]

copyfiles = jpegfiles
#jpegfiles = files_with_ext(mypath, '.jpg') # get all the files with extentsion

remove = []
for f in copyfiles:
#    dest = os.path.join(newpath, os.path.basename(f))
    if os.path.basename(f) not in ages:
#        remove.append(f)
        os.remove(f)
#       shutil.copy(f, dest)
print(len(remove))
