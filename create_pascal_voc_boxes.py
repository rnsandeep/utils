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
import multiprocessing
from time import sleep

def readBoxes(fname, box, new_path, width, height):
    labelledObjects = dict()
    labelledObjects['aeroplane'] = [box]
    newxml = write_xml(fname, labelledObjects, width, height)
    g = open(new_path,'w')
    g.write(newxml)
    g.close()


def write_xml(file_name, objects, width, height):
    ann = "<annotation><folder>FGVC</folder><filename>"+file_name+"</filename><segmented>0</segmented><source><database>FGVC-DB</database><annotation>FGVC-DB</annotation><image>FGVC-DB</image><flickrid>HealloSkin</flickrid></source><owner><flickrid>fgvc</flickrid><name>fgvc</name></owner>"
    ann += "<size><width>"+str(width)+"</width><height>"+str( height)+"</height><depth>3</depth></size>"
    for obj in objects:
      for ins in objects[obj]:
          ann += "<object><name>"+obj+"</name><pose>frontal</pose><truncated>0</truncated><difficult>0</difficult><bndbox><xmin>"+str(ins[0])+"</xmin><ymin>"+str(ins[1])+"</ymin><xmax>"+str(ins[2])+"</xmax><ymax>"+str(ins[3])+"</ymax></bndbox></object>"
    ann += "</annotation>"
    return ann


if __name__ == '__main__':
    mypath = sys.argv[1]
    outputpath = sys.argv[2]
    if not os.path.exists(outputpath):
       os.makedirs(outputpath)
    #images = [os.path.join(mypath,f) for f in listdir(mypath) if isfile(join(mypath, f))] 
    images = open('images_box.txt','r').readlines()
    count  = 0    
    totalCount = 0
    jobs = []
    for image in images:
        fields = image.strip().split()
        image = fields[0]
        box = [int(b) for b in fields[1:]]
        name = os.path.join(mypath, image.strip()+'.jpg')
        print name
        I = cv2.imread(name)
        width, height = I.shape[:-1]
        p = multiprocessing.Process(target=readBoxes, args=(image+'.jpg', box,  os.path.join(outputpath, os.path.basename(image)+'.xml'), width, height, ))
        jobs.append(p)
        totalCount = totalCount + 1
        p.start()

