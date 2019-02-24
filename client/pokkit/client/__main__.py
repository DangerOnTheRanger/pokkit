import errno
import os
import stat
import sys

import fuse
from fuse import Fuse, Stat


fuse.fuse_python_api = (0, 2)


class RepoStat(Stat):
    def __init__(self):
        self.st_mode = 0
        self.st_ino = 0
        self.st_dev = 0
        self.st_nlink = 0
        self.st_uid = 0
        self.st_gid = 0
        self.st_size = 0
        self.st_atime = 0
        self.st_mtime = 0
        self.st_ctime = 0


test_string = "Hello from Pokkit!"


class RepoFilesystem(Fuse):
    def getattr(self, path):
        st = RepoStat()
        if path == "/":
            st.st_mode = stat.S_IFDIR | 0o755
        elif path == "/example":
            st.st_mode = stat.S_IFREG | 0o444
            st.st_size = len(test_string)
        else:
            return -errno.ENOENT
        return st
            
    def readdir(self, path, offset):
        for entry in ".", "..", "example":
            yield fuse.Direntry(entry)
    def open(self, path, flags):
        pass
    def read(self, path, size, offset):
        slen = len(test_string)
        if offset < slen:
            # still have stuff to read
            if offset + size > slen:
                # read everything left, but no more
                size = slen - offset
            result_buffer = test_string[offset:offset + size]
        else:
            result_buffer = ""
        return result_buffer
        

def main():
    sys.stdout.write("Hello World!\n")
    sys.stdout.flush()
    os.mkdir("/pokkit-mount")
    fuse_server = RepoFilesystem(version="%prog " + fuse.__version__,
                                 dash_s_do="setsingle")
    fuse_server.parse(["/pokkit-mount"], errex=1)
    fuse_server.main()
    sys.stdout.write("Finished!\n")
    sys.stdout.flush()


if __name__ == "__main__":
    main()
