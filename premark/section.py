from typing import Optional, Union
from pathlib import Path
from dataclasses import dataclass

from .utils import contents_of_file_coercible


@dataclass
class FullSectionEntry:
    '''
    The metadata representing a section of a multi-part presentation.
    '''
    filename: str
    title: Optional[str] = None


SectionFilename = str
SectionEntry = Union[SectionFilename, FullSectionEntry]

class Section:

    def __init__(
        self,
        filename: Union[Path, str],
        title: Optional[str] = None,
    ):
        self.filename = Path(filename)
        self.title = title

    @classmethod
    def from_entry(
        cls,
        entry: SectionEntry,
        parent_dir: Union[Path, str, None] = None,
    ) -> 'Section':
        if isinstance(entry, str):
            filename = entry
            title = None
        else:
            filename = entry.filename
            title = entry.title
        if parent_dir is not None:
            parent_dir = Path(parent_dir)
            filename = parent_dir / filename
        return cls(filename=filename, title=title)

    def markdown(self):
        md = contents_of_file_coercible(self.filename)
        if self.title:
            return (
                'class: center, middle\n'
                f'## #{1}\n'  # TODO: this should be fixed to be the section number
                f'# {self.title}\n'
                '---\n'
                f'{md}'
            )
        else:
            return md
