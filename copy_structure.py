import sys, shutil, os
import random
import string, pickle
from file_utils import files_with_ext, create_dir
from PIL import Image

mypath = sys.argv[1]
newpath = sys.argv[2]

create_dir(newpath)

paths = [s.strip() for s in open(sys.argv[3],'r').readlines()]

count = 0
for idx, path in enumerate(paths):
    path = path[2:]
    folder = os.path.join(newpath, os.path.dirname(path))

    create_dir(folder)
    dest = os.path.join(folder, os.path.basename(path))
    src  = os.path.join(mypath, os.path.basename(path))
    sys.stdout.write('count: {:d}/{:d} \r' \
                             .format(idx, len(paths)))
    sys.stdout.flush()
    try:
      if not os.path.exists(dest) and os.path.exists(src):
       if Image.open(src) is None:
           continue
       shutil.copy(src, dest)
    except Exception as ex:
      count = count +1
      print(ex)


print("count of missed:", count)
