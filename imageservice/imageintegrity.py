import subprocess
import os


def verify(f):

    if not os.path.isfile(f):
        return(
            False,
            "{0:s} is not a file".format(f)
        )

    r = subprocess.run(["jpeginfo", "-c", f], stdout=subprocess.PIPE)

    if r.returncode:
        return(
            False,
            r.stdout.decode("utf-8").strip()
        )
    else:
        return(True, None)
