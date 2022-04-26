from pathlib import Path
from dataclasses import dataclass
from typing import Any, Union, Optional, Type, Iterator
from typing import Protocol, runtime_checkable, TypeVar

import yaml

from .presentation import Presentation


P = TypeVar('P', bound='_PartialConfig')


@runtime_checkable
class Readable(Protocol):
    def read(self) -> Union[str, bytes]: ...


SectionList = list[dict[str, str]]


@dataclass
class SectionDefinition:
    file: Path
    title: Optional[str] = None
    autotitle: Optional[bool] = None  # If None, treated as True if title is not None.

    def __post_init__(self):
        # Assume files without suffixes that don't exist should be .md files.
        if '.' not in str(self.file) and not self.file.exists():
            new_file = self.file.with_suffix('.md')
            #logger.info(f'Inferring .md suffix: changing {self.file} to {new_file}')
            self.file = new_file

    def should_autotitle(self):
        return self.autotitle if self.autotitle is not None else bool(self.title)

    def make_presentation(self, section_num: int = None) -> 'Presentation':
        markdown = self.file.read_text()
        # Create the auto-generated section title slide.
        if self.should_autotitle():
            if section_num is None:
                msg = ('Must provide a `section_num` argument to create presentations '
                       'from autotitled SectionDefinitions.')
                raise ValueError(msg)
            markdown = ('class: center, middle\n'
                        '## #{section_num}\n'
                        '# {self.title}\n'
                        '---\n'
                        f'{markdown}')
        return Presentation(markdown)


class _PartialConfig:

    def __init__(
        self,
        config_dict: dict[str, Any],
    ):
        self._config_dict = config_dict

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
        return iter(self._config_dict)

    def __getitem__(self, key: str) -> Any:
        return self._config_dict[key]
