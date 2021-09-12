import sys
from functools import reduce
from operator import add
from pathlib import Path
import logging
from typing import Union, List, Iterable, NamedTuple, Optional
from pkg_resources import resource_filename
from dataclasses import dataclass

from jinja2 import Template
import yaml

if sys.version_info >= (3, 8):
    from typing import Final
else:
    from typing_extensions import Final

PKG_NAME = 'premark'
logger = logging.getLogger(__name__)


class DefaultSettings(NamedTuple):
    javascript: str
    html_template: Path
    stylesheet: Path
    title: str
    metafile: str


DEFAULTS: Final = DefaultSettings(
    javascript="""
        <script src="https://remarkjs.com/downloads/remark-latest.min.js"></script>
        <script>
            var slideshow = remark.create({
                ratio: '16:9',
                slideNumberFormat: '(%current%/%total%)',
                countIncrementalSlides: false,
                highlightLines: true
            });
        </script>
    """,
    html_template=Path(resource_filename(PKG_NAME, 'templates/default.html')),
    stylesheet=Path(resource_filename(PKG_NAME, "templates/default.css")),
    title='Premark Presentation',
    metafile='sections.yaml',
)


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


class Presentation:
    '''
    An unrendered RemarkJS presentation.
    '''
    markdown: str
    html_template: str
    stylesheet_template: str

    def __init__(
        self,
        markdown: Union[str, Path],
        html_template: Union[str, Path] = DEFAULTS.html_template,
        stylesheet: Union[str, Path] = DEFAULTS.stylesheet,
    ):
        '''
        Create a new Presentation.

        Parameters
        ----------
        markdown
            The markdown from which to render the presentations. If a Path object, is
            interpreted as a file containing the markdown. If a string, is interpreted
            as the literal markdown.
        html_template
            The HTML in which to insert the markdown. If a Path object, is interpreted
            as a file containing the HTML. If a string, is interpreted as the literal
            HTML.
        stylesheet
            The CSS to include in the eventual rendered HTML. If a Path object, is
            interpreted as a file containing the CSS. If a string, is interpreted as the
            literal CSS code.
        '''
        if isinstance(markdown, Path):
            markdown = markdown.read_text()
        if isinstance(html_template, Path):
            html_template = html_template.read_text()
        if isinstance(stylesheet, Path):
            stylesheet = stylesheet.read_text()
        self.markdown = markdown
        self.html_template = html_template
        self.stylesheet = stylesheet

    def to_html(self, title: str = DEFAULTS.title) -> str:
        '''
        Convert the presentation to HTML.

        Parameters
        ----------
        title
            The name to be used in the title tag in the resulting HTML.

        Returns
        -------
        str
            An HTML rendering of the presentation.
        '''
        template = Template(self.html_template)
        stylesheet_html = f"<style>\n{self.stylesheet}\n</style>"
        return template.render(
            title=title,
            markdown=self.markdown,
            stylesheet=stylesheet_html,
            js=DEFAULTS.javascript,
        )

    def __add__(self, other: 'Presentation') -> 'Presentation':
        '''Concatenate presentations.'''
        if not isinstance(other, self.__class__):
            return NotImplemented
        html_matches = (self.html_template == other.html_template)
        style_matches = (self.stylesheet == other.stylesheet)
        if html_matches and style_matches:
            merged_markdown = self.markdown + '\n---\n' + other.markdown
            return self.__class__(
                markdown=merged_markdown,
                html_template=self.html_template,
                stylesheet=self.stylesheet,
            )
        else:
            msg = ('Cannot concatenate presentations unless they have the same HTML and'
                   'stylesheet.')
            raise TypeError(msg)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        else:
            md_matches = (self.markdown == other.markdown)
            html_matches = (self.html_template == other.html_template)
            style_matches = (self.stylesheet == other.stylesheet)
            return (md_matches and html_matches and style_matches)

    @classmethod
    def from_presentations(
        cls,
        presentations: Iterable['Presentation'],
    ) -> 'Presentation':
        '''
        Create a single presentations by merging others together.

        Parameters
        ----------
        presentations
            An iterable of Presentation objects

        Returns
        -------
        Presentation
            The resulting, merged presentation
        '''
        # Because '+' is overloaded to concatenate, this merges the inputs.
        return reduce(add, presentations)

    @classmethod
    def from_directory(
        cls,
        directory: Union[str, Path],
        metafile: str = DEFAULTS.metafile,
    ) -> 'Presentation':
        '''
        Create a slideshow from multiple markdown files in a folder.

        Parameters
        ----------
        directory
            The directory where the markdown files are stored. Should be a Path object
            or a string that can be treated as a path.
        metafile
            The name of the file in that directory that defines the order in which to
            stitch together the markdown files.

        Returns
        -------
        Presentation
            A new presentation based on the files in the input directory
        '''
        if not isinstance(directory, Path):
            directory = Path(directory)
        metafile_path = directory / metafile

        try:
            with open(metafile_path, 'rt') as f:
                metadata = yaml.load(f, Loader=yaml.SafeLoader)
        except FileNotFoundError as exc:
            msg = f'metafile "{metafile}" not found in directory'
            raise ValueError(msg) from exc
        # The should contain a dictionary with a 'sections' key, the value of which is a
        # list of dictionaries, along with optional additional keys 'html_template' and
        # 'stylesheet'.
        try:
            sections = metadata['sections']
        except (KeyError, TypeError) as exc:
            msg = "Expected to find 'sections' heading in metafile"
            raise KeyError(msg) from exc
        if 'html_template' in metadata:
            html_template = Path(metadata['html_template'])
        else:
            html_template = DEFAULTS.html_template
        if 'stylesheet' in metadata:
            stylesheet = Path(metadata['stylesheet'])
        else:
            stylesheet = DEFAULTS.stylesheet
        # If we have a list of {'file': str} pairs (vs just a list of strings), we need
        # to extract the filenames.
        if isinstance(sections[0], dict):  # metadata is List[Dict[str, str]]
            try:
                section_defs = [
                    SectionDefinition(
                        file=(directory / entry['file']),
                        title=entry.get('title'),
                        autotitle=entry.get('autotitle')
                    )
                    for entry in sections
                ]
            except KeyError:
                msg = 'Section entries must contain a "file" key'
                raise KeyError(msg)
        else:  # sections is List[str], hopefully
            section_defs = [SectionDefinition(directory / s) for s in sections]
        # Check the files exist and then stitch them together.
        section_num = 1
        presentations: List[Presentation] = []
        for section in section_defs:
            if section.should_autotitle():
                prez = section.make_presentation(section_num)
                section_num += 1
            else:
                prez = section.make_presentation()
            presentations.append(prez)
        final_prez = Presentation.from_presentations(presentations)
        final_prez.html_template = Path(html_template).read_text()
        final_prez.stylesheet = Path(stylesheet).read_text()
        return final_prez
