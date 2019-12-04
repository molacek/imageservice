import subprocess
import os
from io import BytesIO


def verify_integrity(f):

    if not os.path.isfile(f):
        return(False, "{0:s} is not a file".format(f))

    r = subprocess.run(["jpeginfo", "-c", f], stdout=subprocess.PIPE)

    if r.returncode:
        return(False, r.stdout.decode("utf-8").strip())
    else:
        return True


def image_buffer(filename, filesize=None, force=False):

    # Filezeise limit is set
    if filesize:
        statinfo = os.stat(filename)
        if statinfo.st_size > filesize or force:
            if force:
                print(f"Image {filename} forced to be processed by ImageMagick")
            else:
                print(f"Downsizing {filename} to {filesize} bytes")
            r = subprocess.run([
                "convert",
                filename,
                "-define",
                "jpeg:extent={0:d}".format(filesize),
                "jpeg:-"
            ], stdout=subprocess.PIPE)

            return BytesIO(r.stdout)

    with open(filename, 'rb') as f:
        return(BytesIO(f.read()))
