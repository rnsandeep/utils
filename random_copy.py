import sys, shutil, os
import random
import string
from file_utils import getfiles, create_dir

def random_str(N):
    # generate random string of length N
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))

mypath = sys.argv[1]
newpath = sys.argv[2]

create_dir(mypath)
jpegfiles = files_with_ext(mypath, '.jpg') # get all the files with extentsion

# fo random shuffle of files
random.shuffle(files)

number = int(sys.argv[3])

if number < len(onlyfiles):
    copyfiles = onlyfiles[:number]
else:
    copyfiles = onlyfiles*(int(number/len(onlyfiles))+1)
    print(len(copyfiles))
    copyfiles = copyfiles[:number]


for f in copyfiles:
    dest = os.path.join(newpath, os.path.basename(f))
    if os.path.exists(dest):
       newname = os.path.join(newpath, random_str(3)+os.path.basename(f))
       print(newname)
       shutil.copy(f, newname)
    else:
       shutil.copy(f, dest)
