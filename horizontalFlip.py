import sys, shutil, os
import random
import string
from file_utils import files_with_ext, create_dir
from PIL import Image
import multiprocessing

def random_str(N):
    # generate random string of length N
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))

mypath = sys.argv[1]
newpath = sys.argv[2]

create_dir(newpath)

jpegfiles = files_with_ext(mypath, '.jpg') # get all the files with extentsion

def flip_image(jpeg):
    try:
       img = Image.open(jpeg).transpose(Image.FLIP_TOP_BOTTOM)
       img.save(os.path.dirname(jpeg)+ '/hflip_'+ os.path.basename(jpeg))
    except Exception  as ex:   
       print(ex) 


if __name__ == '__main__':

    jobs = []
    print("processing:")
    for idx, jpeg in enumerate(jpegfiles):
        p = multiprocessing.Process(target=flip_image, args=(jpeg, ))
        jobs.append(p)
        p.start()
        sys.stdout.write('count: {:d}/{:d}  \r' \
                             .format(idx, len(jpegfiles)))
        sys.stdout.flush()        
