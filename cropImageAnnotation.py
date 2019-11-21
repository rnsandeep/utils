import cv2, sys, os
from tqdm import tqdm 
import numpy as np
import multiprocessing
from readXML import read_xml, write_xml

def readImage(image):
    I = cv2.imread(image)
    w, h = I.shape[:2]
    return I, w, h

def selectRandomCrop(w, h):
    topLeftX = np.random.randint(int(h*0.3), size=1)
    topLeftY = np.random.randint(int(w*0.3), size=1)

    bottomRightX = h - np.random.randint(int(h*0.3), size=1)
    bottomRightY = w - np.random.randint(int(w*0.3), size=1)

    return int(topLeftX), int(topLeftY), int(bottomRightX), int(bottomRightY)


def divideImage(w, h, num):
    Iwidth, Iheight = w, h
    height = int(Iheight/num)
    width = int(Iwidth/num)
    coords = []
    for i in range(0, Iheight, height):
        for j in range(0, Iwidth, width):
            box = (j, i, j+width, i+height)
            coords.append([int(c) for c in box])
    return coords    




def cropImage(img, tx, ty, bx, by):
    crop = img[ty:by, tx:bx]
    return crop


def cropXML(xml, w, h, tx, ty, bx, by, idx):
    labelledObjects = read_xml(xml)
    term = "crop" +str(idx)+"_"
    file_name = term + os.path.basename(xml).split('.xml')[0] + '.jpg'
    ann = write_xml(file_name, labelledObjects, w, h, tx, ty, bx, by)
    return ann


def completeProcess(image):
    image = image.strip()
    I, w, h = readImage(image)
    four_coords = divideImage(w, h, 2)
    for idx in range(4):
        tx, ty, bx, by = four_coords[idx] #selectRandomCrop(w, h)
        cropImg = cropImage(I, tx, ty, bx, by)
        xml = os.path.join(xmlPath, os.path.basename(image).split('.jpg')[0] + '.xml')
        if not os.path.exists(xml):
            return 
        xmlCrop = cropXML(xml, w, h, tx, ty, bx, by, idx)
        saveXmlPath = os.path.join(saveXMLS, "crop" + str(idx)+ "_" + os.path.basename(image).replace('.jpg', '.xml'))
        saveImgPath = os.path.join(saveIMGS, "crop"+ str(idx) + "_" +os.path.basename(image))
        g = open(saveXmlPath, 'w')
        g.write(xmlCrop)
        g.close()  
        cv2.imwrite(saveImgPath, cropImg)


images = open(sys.argv[1], 'r').readlines()
xmlPath = sys.argv[2]
saveXMLS = sys.argv[3]
saveIMGS = sys.argv[4]

if not os.path.exists(saveXMLS):
    os.makedirs(saveXMLS)

if not os.path.exists(saveIMGS):
    os.makedirs(saveIMGS)

totalCount = 0
jobs = []
for image in tqdm(images):
    p = multiprocessing.Process(target=completeProcess, args=(image, ))
    jobs.append(p)
    totalCount = totalCount + 1
    p.start()
