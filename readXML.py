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

    return labelledObjects

def write_xml(file_name, objects, width, height, tx, ty, bx, by):
    ann = "<annotation><folder>CELEB</folder><filename>"+file_name+"</filename><segmented>0</segmented><source><database>Heallo Face DB</database><annotation>Healo Face DB</annotation><image>Heallo Celeb IMDB</image><flickrid>HealloSkin</flickrid></source><owner><flickrid>HealloSkin</flickrid><name>Heallo</name></owner>"
    ann += "<size><width>"+str(width)+"</width><height>"+ str(height)+"</height><depth>3</depth></size>"
    for obj in objects:
        for ins in objects[obj]:
            if int(ins[0]) > tx and int(ins[1]) > ty and int(ins[2]) < bx and int(ins[3]) < by:
                x1 = str(int(ins[0]) - tx)
                y1 = str(int(ins[1]) - ty)
                x2 = str(int(ins[2]) - tx)
                y2 = str(int(ins[3]) - ty)

                ann += "<object><name>"+obj+"</name><pose>frontal</pose><truncated>0</truncated><difficult>0</difficult><bndbox><xmin>"+ x1 +"</xmin><ymin>"+ y1 +"</ymin><xmax>"+ x2 +"</xmax><ymax>"+ y2 +"</ymax></bndbox></object>"
    ann += "</annotation>"
    return ann

