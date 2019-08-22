#!/usr/bin/python
from xml.dom import minidom
import xml.etree.cElementTree as ET, csv,sys,ntpath,pickle,os,traceback,multiprocessing,cv2,numpy as np
from removeSkipXmls import skipXmls
def makeXML(basefilename,imagesFolder,xmlFolder,outputFolder):

    try:
        image = cv2.imread(imagesFolder+ "/" +basefilename+ ".jpg")
        print "Loaded ", imagesFolder + "/" + basefilename+ ".jpg"
        print image.shape
    except:
        print "Image reading failed ", imagesFolder + "/" + basefilename 
       	return

    annotation = ET.Element("annotation")

    folder = ET.SubElement(annotation, "folder").text = "CELEB"
    filename = ET.SubElement(annotation, "filename").text = basefilename + ".jpg"
    segmented = ET.SubElement(annotation, "segmented").text = "0"

    source = ET.SubElement(annotation, "source")
    owner = ET.SubElement(annotation, "owner")
    size = ET.SubElement(annotation, "size")

    ET.SubElement(source, "database").text = "Heallo Face DB"
    ET.SubElement(source, "annotation").text = "Healo Face DB"
    ET.SubElement(source, "image").text = "Heallo Celeb IMDB"
    ET.SubElement(source, "flickrid").text = "HealloSkin"

    ET.SubElement(owner, "flickrid").text = "HealloSkin"
    ET.SubElement(owner, "name").text = "Heallo"

    ET.SubElement(size, "width").text = str(image.shape[1])
    ET.SubElement(size, "height").text = str(image.shape[0])
    ET.SubElement(size, "depth").text = str(image.shape[2])

    doc = minidom.parse( xmlFolder + "/" + basefilename + ".xml")
    objects = doc.getElementsByTagName("object")
    for one_object in objects:
        
        object_name = one_object.getElementsByTagName("name")[0]
        print( str(object_name.firstChild.data))
        deleted = one_object.getElementsByTagName("deleted")[0]
        isDeleted = int(deleted.firstChild.data)
        
        if str(object_name.firstChild.data) not in {"come-region","mole-exact","ascar-region","oscar-region","darkspot-region","pimple-region"}:
            continue

        if isDeleted == 1:
            continue
        
        polygon = one_object.getElementsByTagName("polygon")[0]
        points = polygon.getElementsByTagName("pt")
        x_list = []
        y_list = []

        for point in points:
            x_list.append(int(point.getElementsByTagName("x")[0].firstChild.data))
            y_list.append(int(point.getElementsByTagName("y")[0].firstChild.data))

        xmin = np.amin(x_list)
        ymin = np.amin(y_list)
        xmax = np.amax(x_list)
        ymax = np.amax(y_list)
    #    print "Polygon to bounding box ",xmin,xmax,ymin,ymax

        if xmax>=image.shape[1] or xmin>=image.shape[1] or ymax>=image.shape[0] or ymin>=image.shape[0]:
            print "Invalid bounding box"
            continue

        Object1 = ET.SubElement(annotation, "object")
        ET.SubElement(Object1, "name").text = object_name.firstChild.data
        ET.SubElement(Object1, "pose").text = "frontal"
        ET.SubElement(Object1, "truncated").text = "0"
        ET.SubElement(Object1, "difficult").text = "0"

        box1 = ET.SubElement(Object1, "bndbox")
        ET.SubElement(box1, "xmin").text = str(xmin)
        ET.SubElement(box1, "ymin").text = str(ymin)
        ET.SubElement(box1, "xmax").text = str(xmax)
        ET.SubElement(box1, "ymax").text = str(ymax)

    tree = ET.ElementTree(annotation)
    xmlFilename = outputFolder+basefilename+".xml"
    tree.write(xmlFilename)
    print "XML Processed ", xmlFilename

if __name__ == '__main__':
    
    # input folder
    imagesFolder = sys.argv[1]
    xmlFolder = sys.argv[2]	
    outputFolder = "Annotations/"
    if not os.path.exists(outputFolder):
        os.makedirs(outputFolder)
    f,skip_no=skipXmls(os.path.abspath(xmlFolder),'fileList.txt') 

    jobs = []
    totalCount = 0
    for filename in f:       
        p = multiprocessing.Process(target=makeXML, args=(filename,imagesFolder,xmlFolder,outputFolder,))
        jobs.append(p)
        totalCount = totalCount + 1
        p.start()
    print('%d files are skipped'%skip_no)
