from pathlib import Path
from typing import Any, Union, Mapping, Type, Iterator
from typing import Protocol, runtime_checkable, TypeVar
from pkg_resources import resource_filename

import yaml


P = TypeVar('P', bound='_PartialConfig')


@runtime_checkable
class Readable(Protocol):
    def read(self) -> Union[str, bytes]: ...


class _PartialConfig:

    def __init__(
        self,
        config: Mapping[str, Any],
    ):
        self._config_map = config

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

    def __iter__(self) -> Iterator[str]:
        return iter(self._config_map)

    def __getitem__(self, key: str) -> Any:
        return self._config_map[key]


default_config = _PartialConfig.from_file(resource_filename('premark', 'config.yaml'))
