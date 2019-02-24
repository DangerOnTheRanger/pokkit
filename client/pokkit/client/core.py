from pathlib import Path
import yaml
import typing
from . import util


# TOOD: import this
class FileResource(object):
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

                # conf file
                **yaml.load(f),
            }
        self.config['app_dir'] = Path(self.config['app_dir']).expanduser()
        self.config['app_dir'].mkdir(exist_ok=True)
        self.config['old_dir'] = Path(self.config['app_dir']) / 'old'
        self.config['old_dir'].mkdir(exist_ok=True)
        self.config['cache_dir'] = Path(self.config['app_dir']) / 'cache'
        self.config['cache_dir'].mkdir(exist_ok=True)
        self.config['temp_dir'] = Path(self.config['app_dir']) / 'temp'
        self.config['temp_dir'].mkdir(exist_ok=True)

    def get_path(fr: FileResource) -> Path:
        '''Returns a path to a copy of the data _as it is to the client_'''
        name = '-'.join(
            util.sanitize_fname(component)
            for component in get_components(fr)
        )
        return self.config['cache_dir'] / name

    def get_old_path(fr: FileResource) -> Path:
        '''Returns a path to a copy of the data _as it is on the server_'''
        # TODO: make a copy of fr in the location returned by this function before modifying it
        name = '-'.join(
            util.sanitize_fname(component)
            for component in get_components(fr)
        )
        return self.config['old_dir'] / name


# this is a singleton, I guess
core = Core()
