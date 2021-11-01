from collections import ChainMap
from pathlib import Path
from dataclasses import dataclass
from typing import Any, Union, Optional, List, Dict, TypedDict, Final

import yaml

from .presentation import Presentation


SectionList = List[Dict[str, str]]

CONFIG_ELEMENT_TYPES = {
    'source': Path,
    'sections': SectionList,
    'css_file': Path,
    'html_template_file': Path,
    'output_file': Path,
}


# Define some TypedDicts to specify what configuration dictionaries look like.
class ConfigDict(TypedDict):
    source: Path
    sections: SectionList # Only set if source is a folder
    css_file: Path
    html_template_file: Path
    output_file: Path # If unset, output becomes stdout


@dataclass
class SectionDefinition:
    file: Path
    title: Optional[str] = None
    autotitle: Optional[bool] = None  # If None, treated as True if title is not None.

    def __post_init__(self):
        # Assume files without suffixes that don't exist should be .md files.
        if '.' not in str(self.file) and not self.file.exists():
            new_file = self.file.with_suffix('.md')
            logger.info(f'Inferring .md suffix: changing {self.file} to {new_file}')
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
                        f'## #{section_num}\n'
                        f'# {self.title}\n'
                        '---\n'
                        f'{markdown}')
        return Presentation(markdown)


class ConfigChain(ChainMap):

    # def __init__(
        # self,
        # maps: Iterable[Mapping[str, Any]],
    # ):
        # self.config_map = ChainMap(*sources)
        # self.sources = self.config_map.map
        # super().__init__(*sources)

    @classmethod
    def from_file(cls, filepath: Path) -> 'ConfigChain':
        ...

    @classmethod
    def load(
        cls,
        file: Union[Path, str],
        cli_args: ConfigDict,
        force_valid: bool = True,
    ) -> 'Configuration':
        # File should be a yaml file or the contents of one
        if isinstance(file, Path):
            file = file.read_text()
        raw_conf = yaml.load(file, Loader=yaml.SafeLoader)
        raw_conf.update(cli_args)
        return cls(raw_conf, force_valid=force_valid)

    def __getitem__(self, index: Any) -> Any:
        return self.config_lkp[index]

    def __add__(self, other: 'Configuration') -> 'Configuration':
        return self.__class__.from_mappings(self.config_map, other.config_map)

    def validate(self, raise_=True):
        ... # What's it mean to be valid?
        raise NotImplementedError
        if not valid:
            if raise_:
                raise TypeError('Invalid configuration specified')
            else:
                return False
        else:
            return True

def get_config_from_file(file: Union[Path, str]) -> ConfigDict:
    '''
    Load a config file's contents and validate; return config as a dictionary.
    '''
    if isinstance(file, str):
        file = Path(file)
    contents = file.read_text()
    conf = yaml.load(contents, Loader=yaml.SafeLoader)

    if not isinstance(conf, dict):
        msg = f'Invalid yaml config file "{file}"; file contents must be a mapping.'
        raise TypeError(msg)
    keys = set(conf.keys())
    expected_keys = set(CONFIG_ELEMENT_TYPES.keys())
    if not keys.issubset(expected_keys):
        unexpected_keys = keys - expected_keys
        msg = f'Unexpected keys {unexpected_keys} found in config file.'
        raise ValueError(msg)

    for key in conf:
        expected_type = CONFIG_ELEMENT_TYPES.get(key)
        if expected_type is None:
            msg = f'Unexpected key {key} found in config file.'
            raise ValueError(msg)
        if expected_type == Path:
            # Coerce elements to be Paths if that's the expected type.
            try:
                conf[key] = Path(conf[key])
            except TypeError as exc:
                msg = (
                    f'Unable to convert "{conf[key]}", the value of key "{key}", '
                    'to a path'
                )
                raise TypeError(msg) from exc
        elif expected_type == SectionList:
            value = conf[key]
            try:
                # Check it's a List[Dict[str, str]]
                assert isinstance(value, list)
                assert all(isinstance(elem, dict) for elem in value)
                assert all(isinstance(elem_key, str) and isinstance(elem_val, str)
                           for elem in value for (elem_key, elem_val) in elem.items())
            except AssertionError as exc:
                msg = (
                    f'Expected value of key "{key}" to be of type List[Dict[str, str]]'
                )
                raise TypeError(msg) from exc
    return cast(ConfigDict, conf)


def get_config_from_dict(dct: dict) -> ConfigDict:
    '''
    Take a dictionary containing a config and validate it.
    '''
    ...
