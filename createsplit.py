import shutil, os
from file_utils import files_with_ext, create_dir
import sys
from random import shuffle


xmls = files_with_ext(sys.argv[1],'.xml')

imagesPath = sys.argv[2]
#print(xmls[0])
xmls = [xml.split('/')[-1].split('.xml')[0] for xml in xmls]

xmls = [xml for xml in xmls if os.path.exists(os.path.join(imagesPath, xml+'.jpg'))]
shuffle(xmls)

trainingFraction = 0.90
valFraction = 0.05
testFraction = 0.05

train = []
val = []
test = []

trainLen = int(trainingFraction * len(xmls))
valLen = int(valFraction * len(xmls))
train.extend(xmls[:trainLen])
val.extend(xmls[trainLen:trainLen+valLen])
test.extend(xmls[trainLen+valLen:])

print('Number of training images = %d, and vallidation images = %d and Testing images = %d '%(len(train),len(val), len(test)))

with open('train.txt', 'w') as f:
    for item in train:
        f.write(item + os.linesep)

with open('val.txt', 'w') as f:
    for item in val:
        f.write(item + os.linesep)

with open('test.txt', 'w') as f:
    for item in test:
        f.write(item + os.linesep)

with open('trainval.txt', 'w') as f:
    for item in train+val:
        f.write(item + os.linesep)


