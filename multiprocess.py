#!/usr/bin/env python
import  os, sys, cv2
import shutil
import multiprocessing
from time import sleep

def callme():
    return 


if __name__ == '__main__':
    mypath = sys.argv[1]
    outputpath = sys.argv[2]
    if not os.path.exists(outputpath):
       os.makedirs(outputpath)
    jobs = []
    for idx, image in enumerate(images):
        p = multiprocessing.Process(target=readBoxes, args=())
        jobs.append(p)
        totalCount = totalCount + 1
        p.start()

