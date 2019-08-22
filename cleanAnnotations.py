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
from tqdm import tqdm

CLASSES = ('__background__','come-region','ascar-region','oscar-region','mole-exact','darkspot-region','pimple-region')
def read_xml(xml_path, new_path):
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
       
        
        if int(ymin) >= int(height) or int(ymax) >= int(height) or int(xmin) >= int(xmax) or int(ymin) >= int(ymax) or int(xmin) >= int(width) or int(xmax) >= int(width) :
              flag = False
              continue

        if int(xmin) <=0 or int(ymin) <=0 or int(xmax) <=0 or int(ymax) <=0:
              flag = False
              continue

        if (int(xmax)- int(xmin))*(int(ymax)-int(ymin)) <= 0: 
              flag = False
              continue
   
        box = [xmin, ymin, xmax, ymax]
        bb = []
        for b in box:
            if int(b)  ==0:
                b = 1
            bb.append(b)
        box = (bb[0], bb[1], bb[2] , bb[3])
        if name not in labelledObjects:
            labelledObjects[name] = []
            labelledObjects[name].append(box)
        else:
            labelledObjects[name].append(box)

    if len(labelledObjects.keys())== 0:
        return False, xml_path

    newxml = write_xml(fname, labelledObjects, width, height)
    g = open(new_path,'w')
    g.write(newxml)
    g.close()
    return flag, xml_path


def write_xml(file_name, objects, width, height):
    ann = "<annotation><folder>CELEB</folder><filename>"+file_name+"</filename><segmented>0</segmented><source><database>Heallo Face DB</database><annotation>Healo Face DB</annotation><image>Heallo Celeb IMDB</image><flickrid>HealloSkin</flickrid></source><owner><flickrid>HealloSkin</flickrid><name>Heallo</name></owner>"
    ann += "<size><width>"+width+"</width><height>"+ height+"</height><depth>3</depth></size>"
    for obj in objects:
      for ins in objects[obj]:
          ann += "<object><name>"+obj+"</name><pose>frontal</pose><truncated>0</truncated><difficult>0</difficult><bndbox><xmin>"+str(ins[0])+"</xmin><ymin>"+str(ins[1])+"</ymin><xmax>"+str(ins[2])+"</xmax><ymax>"+str(ins[3])+"</ymax></bndbox></object>"
    ann += "</annotation>"
    return ann


if __name__ == '__main__':
    mypath = sys.argv[1]
    outputpath = sys.argv[2]
    os.makedirs(outputpath)
    images = [mypath+'/'+f for f in listdir(mypath) if isfile(join(mypath, f))] 

    g = open("wrong.txt", "w")
    count  = 0    
    for image in tqdm(images):
        flag, xml_path  = read_xml(image, outputpath+'/'+image.split('/')[-1])
        if  not flag:
            count  = count +1
            g.write(os.path.basename(xml_path)+"\n")    
    g.close()    
    print("no of images in which annotations are wrong", count)
    
