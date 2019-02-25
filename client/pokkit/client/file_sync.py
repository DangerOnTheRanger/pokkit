'''This is the client-side half of the file-sync protocol'''


import io
from pathlib import Path
import os
import shutil
from .core import core, get_components
from . import gui

# TOOD: import this
class FileResource(object):
    pass
class FileContents(object):
    pass
class Diff(bytes):
    pass


# TODO: get these path right
_patch_program = './patch_b'
_diff_program = './diff_b'


def _diff(old_path: Path, new_path: Path) -> bytes:
    proc = subprocess.run(
        [_diff_program, old_path, new_path],
        capture_stdout=True
    )
    return proc.stdout


def _patch(old_path: Path, diff: bytes, new_path: Path):
    proc = subprocess.run(
        [_patch_program, old_path, '/dev/stdin'],
        input=diff,
        capture_stdout=True,
    )
    with open(new_path, 'wb'):
        new_path.write(proc.stdout)


def _download_url(url: str, path: Path):
    # https://stackoverflow.com/a/39217788/1078199
    with requests.get(url, stream=True) as req:
        with open(path, 'wb') as fil:
            shutil.copyfileobj(req.raw, fil)


def _write_fc(fc: FileContents, new_path: Path, tmp: Path):
    if fc.HasField('diff_url'):
        components = get_components(fc)
        old_path = tmp / '-'.join([*components, '-parent'])
        _download_url(fc.diff_url, old_path)
        diff = requests.get(url).content
        # download parent (recursively)
        write_fc(fc.parent, old_path, tmp)
        _patch(old_path, diff, new_path)
        os.remove(old_path)
    else:
        _download_url(fc.content_url, new_path)
    return new_path


def _read_fc(new_path: Path, old_path: Path, old_fc: FileContents):
    # TODO: check hash before downloading. if hash matches, don't download.
    new_fc = FileContents()
    new_fc.parent = old_fc

    diff = _diff(old_path, new_path)
    if len(diff) < os.path.getsize(new_path):
        new_fc.diff_url = Metadata.send_diff(fr, diff)
    else:
        with open(path, 'rb') as fil:
            new_fc.content_url = Metadata.send_content(fr, fil)


def upload(fr: FileResource):
    fr.file_contents = _read_fc(core.fr2path(fc), core.fr2old_path(fc), fr.fc)
    commit_op = types.CommitOp()
    commit_op.add_file.file_resource = fr
    core.fileService.AddCommit(commit_op)


def download(fr: FileResource):
    return _write_fc(fr.fc, core.fr2path(fc), core.config['temp_dir'])

def delete(fr: FileResource):
    # TODO: add an gRPC endpoint
    pass


def acquire_rlock(fr: FileResource) -> bool:
    if fr.branch.solo:
        return True
    else:
        if not core.fileService.IsLocked(fr):
            # multiuser branch, but we got the lock
            core.fileService.SetLockStatus(fr, True)
            return True
            # TODO: set timer
        else:
            # File is locked out
            fr_str = '/'.join(fr.path)
            choice = gui.download_locked_file(fr, fr_str)
            return False


def acquire_wlock(fr: FileResource):
    if fr.branch.solo:
        # solo branch. Go right on ahead
        return True
    else:
        if not core.fileService.IsLocked(fr):
            # multiuser branch, but nobody is locking it the lock
            # This case is unlikely
            return True
        elif fr.lock_status.owner == core.config['user']:
            # multiuser branch, we hold the lock
            # this is likely
            return True
        else:
            # We are locked out
            # This is unlikely
            fr_str = '/'.join(fr.path)
            choice = gui.upload_locked_file(fr, fr_str)
            return False


def release_rlock(fr: FileResource):
    # we need to make sure we own this lock in the first place before we can release it
    if acquire_rlock(fr):
        core.fileService.SetLockStatus(fr, False)
        # TODO: reset rlock timer
    else:
        raise RuntimeError("Attempted to release a lock you don't hold")


def release_wlock(fr: FileResource):
    # we need to make sure we own this lock in the first place before we can release it
    if acquire_wlock(fr):
        core.fileService.SetLockStatus(fr, False)
        # TODO: reset wlock timer
    else:
        raise RuntimeError("Attempted to release a lock you don't hold")
