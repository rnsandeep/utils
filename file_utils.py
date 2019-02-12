import os, shutil

def files_with_ext(mypath, ext):
    files = [os.path.join(mypath, f) for f in os.path.listdir(mypath) if os.path.isfile(os.path.join(mypath, f)) and if os.path.splitext(os.path.join(mypath, f))[1] == ext]
    return files

def cpy_files_dir(files, path):
    if not os.path.exists(path):
       os.makedirs(path)
    for f in files:
        shutil.copy(f, path)

def create_dir(path):
    if not os.path.exists(path):
       os.makedirs(path)
