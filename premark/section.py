from typing import Optional, Union, TypedDict, Iterable, Iterator
from pathlib import Path

from .utils import contents_of_file_coercible


class FullSectionEntry(TypedDict):
    '''
    The metadata representing a section of a multi-part presentation.
    '''
    file: str
    title: Optional[str]
    numbered: bool


SectionFilename = str
SectionEntry = Union[SectionFilename, FullSectionEntry]


class Section:

    def __init__(
        self,
        filename: Union[Path, str],
        title: Optional[str] = None,
        should_number: bool = False,
        number: Optional[int] = None,
    ):
        if (should_number or number is not None) and title is None:
            raise ValueError('Sections without explicit titles cannot be numbered')
        self.filename = Path(filename)
        self.title = title
        self.should_number = should_number
        self.number = number

    @classmethod
    def from_entry(
        cls,
        entry: SectionEntry,
        parent_dir: Union[Path, str, None] = None,
    ) -> 'Section':
        file: Union[Path, str]
        if isinstance(entry, str):
            file = entry
            title = None
            should_number = False
        else:
            if 'file' not in entry:
                raise TypeError('`file` field must be specified for section entries.')
            file = entry['file']
            title = entry.get('title', None)
            # If 'numbered' is omitted from the config, we should assume titled sections
            # should be numbered but others shouldn't
            should_number_default = title is not None
            should_number = entry.get('numbered', should_number_default)
        if parent_dir is not None:
            parent_dir = Path(parent_dir)
            file = parent_dir / file
        return cls(filename=file, title=title, should_number=should_number)

    @classmethod
    def from_entries(
        cls,
        entries: Iterable[SectionEntry],
        parent_dir: Union[Path, str, None],
        starting_number: int = 1,
    ) -> Iterator['Section']:
        '''
        Create sections from entries in a config file.

        Parameters
        ----------
        entries
            An iterable of valid definitions of sections.
        parent_dir
            The base directory that paths to section markdown files are relative to.
        starting_number
            The number of the first numbered section. You may want to override this if
            building a piece of a larger presentation and thus want to continue the
            numbering of a past one.

        Returns
        -------
        A generator of sections
        '''
        current_number = starting_number

        for entry in entries:
            section = cls.from_entry(entry, parent_dir)
            if section.should_number:
                section.number = current_number
                current_number += 1
            yield section

    def markdown(self, number: Optional[int] = None):
        md = contents_of_file_coercible(self.filename)
        if number is None:
            number = getattr(self, 'number', None)
        if number is not None:
            numbering_line = f'## #{self.number}\n'
        else:
            numbering_line = '\n'
        if self.title:
            return (
                'class: center, middle\n' +
                numbering_line +
                f'# {self.title}\n' +
                '---\n' +
                f'{md}'
            )
        else:
            return md
