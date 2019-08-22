from xml.dom import minidom
import sys,os
# Removes the skipped annotations in the given folder
def skipXmls(xmlfolder,outFile=None):
    xmlFormat = ".xml"
    count = 0
    files=[]
    if os.path.exists(outFile): 
        os.remove(outFile)
    for xml in os.listdir(xmlfolder):
        if xml.find(xmlFormat) == -1:
            continue
        doc = minidom.parse(xmlfolder+"/"+xml)
        doSkip = False
        objects = doc.getElementsByTagName("object")
        fname = doc.getElementsByTagName("filename")[0]
        for one_object in objects:  
            name = one_object.getElementsByTagName("name")[0]
            if name.firstChild.data == "skipped":
                doSkip = True
                break
        if doSkip == True:
            count+=1
            continue
        if outFile!=None:
            with open(outFile, 'a') as f3:
                f3.write(os.path.splitext(fname.firstChild.data)[0] + os.linesep)
        files.append(os.path.splitext(fname.firstChild.data)[0])
    print('%d files are skipped'%count)
    print('files are written at %s'%str(outFile))
    return (files,count)

if __name__=='__main__':
    xmlFolder = sys.argv[1]
    outFile=sys.argv[2]
    f,c=skipXmls(xmlFolder,outFile) 
