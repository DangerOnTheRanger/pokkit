import os
import stat
from pathlib import Path
from .core import core
from . import file_sync
from fusepy import FUSE, FuseOSError, Operations


# based on
# https://github.com/skorokithakis/python-fuse-sample/blob/master/passthrough.py
class RepoFS(object):
    def __init__(self):
        self.files = {}

    def access(self, path, mode):
        # Don't know whether file or dir yet

        dr = core.path2dir(Path(path))
        fr = core.path2fr(Path(path))

        if core.fileService.ValidateDirPath(dr):
            # we can always access directories, but possibly not the
            # files in them. (this is even true when directories are
            # locked)
            return 0

        elif core.fileService.ValidateFilePath(dr):
            if mode & os.W_OK != 0 and not acquire_wlock(fr):
                # not only checks, but also acquires
                # if the user calls access, they likely intend to access
                raise FuseOSError(errno.EACCES)
            if mode & (os.R_OK | os.X_OK) != 0 and not acquire_rlock(fr):
                # For the purpose of this FS read implies execute
                raise FuseOSError(errno.EACCES)

            # this means we can access the file and have the appropriate (r or w) lock
            # Let's proactively download it, and mark it as being worked with
            file_sync.download(fr)
            return 0

        else:
            raise FuseOSError(errno.ENOENT)

    def getattr(self, path):
        fr = core.path2fr(Path(path))
        dr = core.path2dir(Path(path))
        if core.fileService.ValidateDirPath(dr):
            return dict(
                st_mode=stat.S_IFDIR | 0o777,
            )
        elif core.fileService.ValidateFilePath(fr):
            # TODO: set size to either size-on-disk or actual-size
            # based on config opt
            return dict(
                st_mode=stat.S_IFREG | 0o777,
            )
        else:
            raise FuseOSError(errno.ENOENT)

    def chmod(self, path, mode):
        fr = core.path2fr(Path(path))
        dr = core.path2dir(Path(path))
        if core.fileService.ValidateDirPath(dr):
            return 0
        elif core.fileService.ValidateFilePath(fr):
            # if I am going to chmod something, I am probably going to
            # write to it. I'll proactively get a write lock.
            fr = core.path2fr(Path(path))
            if acquire_wlock(fr):
                return 0
            else:
                raise FuseOSError(errno.ENOACCESS)
        else:
            raise FuseOSError(errno.ENOENT)


    def chown(self, path, uid, gid):
        # see chmod
        fr = core.path2fr(Path(path))
        dr = core.path2dir(Path(path))
        if core.fileService.ValidateDirPath(dr):
            return 0
        elif core.fileService.ValidateFilePath(fr):
            fr = core.path2fr(Path(path))
            if acquire_wlock(fr):
                return 0
            else:
                raise FuseOSError(errno.ENOACCESS)
        else:
            raise FuseOSError(errno.ENOENT)

    def readdir(self, path, offset):
        dr = core.path2dir(Path(path))

        if core.fileService.ValidateDirPath(dr):
            # . and ..
            yield '.'
            if len(dr.path) > 0:
                yield '..'

            # fetch entries
            for entry in core.fileService.ListDirectory(dr, False, False):
                if entry.hasField('file'):
                    yield entry.file.path[-1]
                else:
                    yield entry.directory.path[-1]

    def open(self, path, flags):
        # this is a pretend file descriptor
        fr = core.path2fr(Path(path))
        if acquire_rlock(fr):
            file_sync.download(fr)
            real_path = core.fr2path(fr)
            return os.open(real_path, flags)
        else:
            raise FuseOSError(errno.ENOACCESS)

    def create(self, path, mode, fi=None):
        fr = core.path2fr(Path(path))
        if acquire_wlock(fr):
            real_path = core.fr2path(fr)
            result = os.open(real_path, os.O_WRONLY | os.O_CREAT, mode)
            if result > 0:
                upload(fr)
                return result
            else:
                raise FuseOSError(-result)
        else:
            raise FuseOSError(errno.ENOACCESS)

    def read(self, path, size, offset, fd):
        fr = core.path2fr(Path(path))
        if acquire_rlock(fr):
            os.lseek(fd, offset, os.SEEK_SET)
            return os.read(fd, length)
        else:
            raise FuseOSError(errno.ENOACCESS)

    def write(self, path, buf, offset, fd):
        fr = core.path2fr(Path(path))
        if acquire_wlock(fr):
            os.lseek(fd, offset, os.SEEK_SET)
            return os.write(fd, buf)
        else:
            raise FuseOSError(errno.ENOACCESS)

    def truncate(self, path, length, fd=None):
        fr = core.path2fr(Path(path))
        if acquire_wlock(fr):
            os.ftruncate(fd, length)
        else:
            raise FuseOSError(errno.ENOACCESS)

    def flush(self, path, fd):
        fr = core.path2fr(Path(path))
        if acquire_wlock(fr):
            result = os.fsync(fd)
            upload(fr)
            return result
        else:
            raise FuseOSError(errno.ENOACCESS)

    def fsync(self, path, datasync, fd):
        fr = core.path2fr(Path(path))
        if acquire_wlock(fr):
            if datasync != 0:
                result = os.fdatasync(fd)
            else:
                result = os.fsync(fd)
            upload(fr)
            return result
        else:
            raise FuseOSError(errno.ENOACCESS)

    def release(self, path, fd):
        result = os.close(fd)
        fr = core.path2fr(Path(path))
        if acquire_wlock(fr):
            return result
        else:
            raise FuseOSError(errno.ENOACCESS)

    def rename(self, old_path, new_path):
        old_fr = core.path2fr(Path(old_path))
        new_fr = core.path2fr(Path(new_path))
        if acquire_wlock(old_fr):
            if acquire_wlock(new_fr):
                new_fr.fc = old_fr.fc
                upload(new_fr)
                delete(old_fr)
                release_wlock(old_fr)
            else:
                pass

    def utimens(self, path, times=None):
        fr = core.path2fr(Path(path))
        if acquire_wlock(fr):
            # TODO: implement actual time-keeping, if we care. Right now,
            # this will just signify the users intent to continue working
            return
        else:
            raise FuseOSError(errno.ENOACCESS)

    def mknod(self, path, mode, device):
        # No need to support making special file objects in our weird fs
        raise FuseOSError(errno.EINVAL)

    # TODO: support rmdir and mkdir. These need to be supported at the
    # gRPC level

    # Parent dirs automagically created because the path "a/b/c/d"
    # turns into the fr for "a-b-c-d" which can be created
    # instantly.

    def mkdir(self, path):
        raise FuseOSError(errno.EINVAL)
    def rmdir(self, path):
        raise FuseOSError(errno.EINVAL)

    # not supporting xattrs (getxattr, listxattr, removexattr)
    # not supporting links (unlink, readlink, symlink)
    # I think I have to support unlink to get rm to work
    # I think I have to support readlink to get . and .. to work
    # not supporting statfs


def run_fuse():
    FUSE(RepoFS(), str(core.config['mount_dir']), nothreads=True, foreground=True)


if __name__ == "__main__":
    run_fuse()
