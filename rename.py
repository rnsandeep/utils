import os, shutil, sys

def files_with_ext(mypath, ext):
    files = [os.path.join(mypath, f) for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f)) and os.path.splitext(os.path.join(mypath, f))[1] == ext]
    return files


images = files_with_ext(sys.argv[1], '.jpg')


for image in images:
    shutil.move(image, image.replace('.jpg', '.xml'))


