import sys, shutil, os
import random
import string
from file_utils import files_with_ext, create_dir
from tqdm import tqdm 
import multiprocessing
mypath = sys.argv[1]

#jpegfiles = [os.path.join(mypath, s.strip()+'.jpg') for s in open(source_text,'r').readlines()]

copyfiles = files_with_ext(mypath, '.jpg') #jpegfiles
#jpegfiles = files_with_ext(mypath, '.jpg') # get all the files with extentsion

from PIL import Image


def checkImage(f):
    try:
        im = Image.open(f)
        s = im.convert('RGB')
    except Exception as ex:
        os.remove(f)

import cv2
jobs = []
for f in tqdm(copyfiles):
    checkImage(f) 
#    p = multiprocessing.Process(target=checkImage, args=(f,))
#    jobs.append(p)
#    p.start()
