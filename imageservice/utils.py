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


def fix_image_errors(filename):
    r = subprocess.run([
        "convert",
        filename,
        "-"
        ], stdout=subprocess.PIPE)
    return BytesIO(r.stdout)


def resize_image(filename, filesize):
        r = subprocess.run([
            "convert",
            filename,
            "-define",
            "jpeg:extent={0:d}".format(filesize),
            "jpeg:-"
        ], stdout=subprocess.PIPE)

        return BytesIO(r.stdout)


def image_buffer(filename, filesize=None):

    # Filezeise limit is set
    if filesize:
        statinfo = os.stat(filename)
        if statinfo.st_size > filesize:
            print(f"Downsizing {filename} to {filesize} bytes")
            return resize_image(filename, filesize)

    if verify_integrity(filename) is not True:
        print(f"Image {filename} seems to broken. Fixing...")
        return fix_image_errors(filename)

    with open(filename, 'rb') as f:
        return(BytesIO(f.read()))
