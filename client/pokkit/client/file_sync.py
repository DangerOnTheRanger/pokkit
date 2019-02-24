'''This is the client-side half of the file-sync protocol

These assume interactions with the user have already been taken care of, and we
_really do_ want to upload/downlad/etc.

'''


import io
from pathlib import Path
import os
import shutil
from .core import core


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


def _read_fc(new_path: Path, old_path: Path, old_fc: FileContents):
    new_fc = FileContents()
    new_fc.parent = old_fc

    diff = _diff(old_path, new_path)
    if len(diff) < os.path.getsize(new_path):
        new_fc.diff_url = Metadata.send_diff(fr, diff)
    else:
        with open(path, 'rb') as fil:
            new_fc.content_url = Metadata.send_content(fr, fil)


def upload_one(fr: ListFileResource):
    fr.file_contents = _read_fc(core.get_path(fc), core.get_old_path(fc), fr.fc)
    commit_op = types.CommitOp()
    commit_op.add_file.file_resource = fr
    core.fileService.AddCommit(commit_op)


def download_one(fr: FileResource):
    _write_fc(fr.fc, core.get_path(fc), core.config['temp_dir'])
