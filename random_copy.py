from random import shuffle
import sys, shutil, os
import random
from os import listdir
from os.path import isfile, join
import string
def random_str(num):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(num))

mypath = sys.argv[1]
newpath = sys.argv[2]
if not os.path.exists(newpath):
    os.makedirs(newpath)
onlyfiles = [os.path.join(mypath, f) for f in listdir(mypath) if isfile(join(mypath, f))]

shuffle(onlyfiles)

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
