import getpass
from pathlib import Path
import yaml
import typing
from . import util


# TOOD: import this
class FileResource(object):
    pass
class Directory(object):
    pass
class BranchResource(object):
    pass
class RepositoryResource(object):
    pass


def get_components(fr: FileResource) -> typing.List[str]:
    return [
        fr.branch.repository.owner,
        fr.branch.repository.name,
        fr.branch.name,
        *fr.path,
    ]


class Core(object):
    def __init__(self):
        with util.open_or_default('./config.yaml', default='{}') as f:
            self.config = {
                # defaults
                'app_dir': '~/.pokkit-client/',
                'lock_delay': 5,
                'user': getpass.getuser(),
                'mount_dir': '/pokkit-mount/',

                # conf file
                **yaml.load(f),
            }

        # computed config values
        self.config['app_dir'] = Path(self.config['app_dir'])
        self.config['cache_dir'] = Path(self.config['app_dir']) / 'cache'
        self.config['old_dir'] = Path(self.config['app_dir']) / 'old_cache'
        self.config['temp_dir'] = Path(self.config['app_dir']) / 'temp'


        # Normalize directory entries to be paths that exist
        for dir_key in ['app_dir', 'old_dir', 'cache_dir', 'temp_dir', 'mount_dir']:
            self.config[dir_key] = Path(self.config[dir_key]).expanduser()
            self.config[dir_key].mkdir(exist_ok=True, parents=True)

    def dir2path(dr: Directory) -> Path:
        pass

    def path2dir(path: Path) -> Directory:
        # resolve . and ..
        pass

    def path2fr(path: Path) -> FileResource:
        pass

    def fr2path(fr: FileResource) -> Path:
        '''Returns a path to a copy of the data _as it is to the client_'''
        name = '-'.join(
            util.sanitize_fname(component)
            for component in get_components(fr)
        )
        return self.config['cache_dir'] / name

    def fr2old_path(fr: FileResource) -> Path:
        '''Returns a path to a copy of the data _as it is on the server_'''
        # TODO: make a copy of fr in the location returned by this function before modifying it
        name = '-'.join(
            util.sanitize_fname(component)
            for component in get_components(fr)
        )
        return self.config['old_dir'] / name


# this is a singleton, I guess
core = Core()
