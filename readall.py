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
import uuid, pickle
import random

CLASSES = ('__background__','come-region','ascar-region','oscar-region','mole-exact','darkspot-region','pimple-region')
def read_xml(object_dict, xml_path, new_path):
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
   
        box = [xmin, ymin, xmax, ymax]
        if name not in labelledObjects:
            labelledObjects[name] = []
            labelledObjects[name].append((box, uuid.uuid4()))
        else:
            labelledObjects[name].append((box, uuid.uuid4()))

    object_dict[fname] = {}
    object_dict[fname]['OBJECTS'] = labelledObjects
    object_dict[fname]['WIDTH'] =  width
    object_dict[fname]["HEIGHT"] =  height

    return object_dict, fname


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
    if not os.path.exists(outputpath):
       os.makedirs(outputpath)
    images = [mypath+'/'+f for f in listdir(mypath) if isfile(join(mypath, f))]

    count  = 0    
    object_dict = {}

    issues = {}
    for image in tqdm(images):
        object_dict, fname = read_xml(object_dict , image, outputpath+'/'+image.split('/')[-1])
        for iss in object_dict[fname]['OBJECTS']:
            if iss not in issues:
                issues[iss] = []
                issues[iss] += [b[1] for b in object_dict[fname]['OBJECTS'][iss]]
            else:
                issues[iss] += [b[1] for b in object_dict[fname]['OBJECTS'][iss]]

    percentage = 5            

    retain = {}

    for iss in issues:
        print(iss, len(issues[iss]))
        boxes = issues[iss]
        random.shuffle(boxes)
        last = len(boxes) -int(len(boxes)*percentage*0.01)
        boxes = boxes[:last]
        retain[iss] = boxes

    for fname in object_dict:
        output_file = os.path.join(outputpath, fname.replace('.jpg', '.xml'))
        objects = object_dict[fname]["OBJECTS"]
        newobjects = {}
        for label in objects:
            newobjects[label] = []
            for box in objects[label]:
                if box[1] in retain[label]:
                    newobjects[label].append(box[0])
        print(output_file)            
        newxml = write_xml(fname, newobjects, object_dict[fname]['WIDTH'], object_dict[fname]['HEIGHT'])
        g = open(output_file,'w')
        g.write(newxml)
        g.close()
    
#    pickle.dump(object_dict, open("allObjects.pkl", "wb"))    
    
