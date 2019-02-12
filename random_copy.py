from random import shuffle
import sys, shutil, os

from os import listdir
from os.path import isfile, join

mypath = sys.argv[1]
newpath = sys.argv[2]
if not os.path.exists(newpath):
    os.makedirs(newpath)
onlyfiles = [os.path.join(mypath, f) for f in listdir(mypath) if isfile(join(mypath, f))]

shuffle(onlyfiles)

number = int(sys.argv[3])

copyfiles = onlyfiles[:number]

for f in copyfiles:
    shutil.copy(f, newpath)
