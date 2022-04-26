import logging
from pkg_resources import resource_filename
from pathlib import Path
from typing import Any, Union, Mapping, Type, Iterator
from typing import Protocol, runtime_checkable, TypeVar

import yaml


P = TypeVar('P', bound='PartialConfig')

def pkg_file(path: str) -> str:
    return resource_filename('premark', path)


@runtime_checkable
class Readable(Protocol):
    def read(self) -> Union[str, bytes]: ...


logger = logging.getLogger(__name__)


class PartialConfig:

    def __init__(
        self,
        config: Mapping[str, Any],
    ):
        def sub_pkg_name(s: str) -> Any:
            '''Replace {{premark}} with the package path.'''
            if isinstance(s, str) and s.startswith('{{premark}}'):
                updated = pkg_file(s.replace('{{premark}}', ''))
                logger.debug('Replacing config value %s with %s', s, updated)
                return updated
            return s
        self._config_map = {
            key: sub_pkg_name(value) for key, value in config.items()
        }
        logger.debug('Created new PartialConfig with keys %s', self.keys())

    @classmethod
    def from_file(
        cls: Type[P],
        file: Union[Readable, Path, str],
    ) -> P:
        '''
        Generate a config from a file or a path to a file.
        '''
        if isinstance(file, Readable):
            contents = file.read()
        else:
            if isinstance(file, str):
                file = Path(file)
            contents = file.read_text()
        return cls.from_yaml(contents)

    @classmethod
    def from_yaml(
        cls: Type[P],
        _yaml: Union[str, bytes],
        /
    ) -> P:
        '''
        Generate a config from a string or bytes of valid yaml.
        '''
        conf = yaml.load(_yaml, Loader=yaml.SafeLoader)
        return cls(conf)

    def items(self) -> Iterator[tuple[str, Any]]:
        return self._config_map.items()

    def keys(self) -> Iterator[str]:
        return self._config_map.keys()

    def values(self) -> Iterator[Any]:
        return self._config_map.values()

    def __iter__(self) -> Iterator[str]:
        return iter(self._config_map)

    def __getitem__(self, key: str) -> Any:
        return self._config_map[key]
