#!/usr/bin/env python
import os
from xml.dom import minidom
os.environ['GLOG_minloglevel'] = '2'
import  os, sys, cv2
import argparse
import shutil
import sys ,os
from os import listdir
from os.path import isfile, join
import numpy as np
from tqdm import tqdm

def read_xml(xml_path):
    flag = True
    doc = minidom.parse(xml_path)
    objects = doc.getElementsByTagName("object")
    fname = doc.getElementsByTagName("filename")[0].firstChild.data
    size = doc.getElementsByTagName("size")[0]
    width = size.getElementsByTagName("width")[0].firstChild.data
    height =  size.getElementsByTagName("height")[0].firstChild.data
    labelledObjects = dict()
    
    for obj in objects:
        name = obj.getElementsByTagName("name")[0].firstChild.data
        xmin = obj.getElementsByTagName("xmin")[0].firstChild.data
        ymin = obj.getElementsByTagName("ymin")[0].firstChild.data
        xmax = obj.getElementsByTagName("xmax")[0].firstChild.data
        ymax = obj.getElementsByTagName("ymax")[0].firstChild.data

        if name not in labelledObjects:
            labelledObjects[name] = 1
        else:
            labelledObjects[name] += 1

    return labelledObjects


if __name__ == '__main__':
    mypath = sys.argv[1]
    images = [mypath+'/'+f for f in listdir(mypath) if isfile(join(mypath, f))] 
    count  = 0  
    counter = dict()
    for image in tqdm(images):
       count  = read_xml(image)
       for key in count:
           if key not in counter:
               counter[key] = count[key]
           else:
               counter[key] += count[key]
    print(counter)           
