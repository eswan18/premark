from pathlib import Path
from dataclasses import dataclass
from typing import Union, Optional, List, Dict, TypedDict, Final

import yaml

from .presentation import Presentation


SectionList = List[Dict[str, str]]

# Define some TypedDicts to specify what configuration dictionaries look like.
class ConfigDict(TypedDict):
    source: Path
    sections: Optional[SectionList] # Only set if source is a folder
    css_file: Path
    html_template_file: Path
    output_file: Optional[Path] # If unset, output becomes stdout

class TotalConfigDict(TypedDict, total=True):
    source: Path
    sections: Optional[SectionList] # Only set if source is a folder
    css_file: Path
    html_template_file: Path
    output_file: Optional[Path] # If unset, output becomes stdout
    

c: ConfigDict = {'source': Path('.'), 'sections': None, 'css_file': Path('.'), 'html_template_file': Path('.')}
d: TotalConfigDict = {'source': Path('.'), 'sections': None, 'css_file': Path('.'), 'html_template_file': Path('.')}

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
                        '## #{section_num}\n'
                        '# {self.title}\n'
                        '---\n'
                        f'{markdown}')
        return Presentation(markdown)


class Configuration:

    def __init__(
        self,
        config_dict: ConfigDict,
        force_valid: bool =True
    ):
        self._config_dict = config_dict
        self.validate(raise_=force_valid)

    @classmethod
    def load(
        cls,
        file: Union[Path, str],
        cli_args: ConfigDict
    ) -> 'Configuration':
        # File should be a yaml file or the contents of one
        if isinstance(file, Path):
            file = file.read_text()
        raw_conf = yaml.load(file, Loader=yaml.SafeLoader)
        raw_conf.update(cli_args)
        return raw_conf # Mypy will likely yell because we don't know what's in the config file

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
