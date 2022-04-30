import logging
from typing import Any, Union, MutableMapping, Mapping, Type, Iterator, TypeVar
from typing import ItemsView, KeysView, ValuesView

import yaml

from .utils import pkg_file, FileCoercible, contents_of_file_coercible


P = TypeVar('P', bound='PartialConfig')


logger = logging.getLogger(__name__)


class PartialConfig(MutableMapping[str, Any]):

    def __init__(
        self,
        config: Mapping[str, Any],
    ):
        def sub_pkg_name(s: str) -> Any:
            '''Replace {{premark}} with the package path.'''
            if isinstance(s, str) and s.startswith('{{premark}}/'):
                updated = pkg_file(s.replace('{{premark}}/', ''))
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
        file: FileCoercible,
    ) -> P:
        '''
        Generate a config from a file or a path to a file.
        '''
        contents = contents_of_file_coercible(file)
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

    def items(self) -> ItemsView[str, Any]:
        return self._config_map.items()

    def keys(self) -> KeysView[str]:
        return self._config_map.keys()

    def values(self) -> ValuesView[Any]:
        return self._config_map.values()

    def __iter__(self) -> Iterator[str]:
        return iter(self._config_map)

    def __getitem__(self, key: str) -> Any:
        return self._config_map[key]

    def __setitem__(self, key: str, value: Any):
        self._config_map[key] = value

    def __delitem__(self, key: str):
        del self._config_map[key]

    def __len__(self) -> int:
        return len(self._config_map)
