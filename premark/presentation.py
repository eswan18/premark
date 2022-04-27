from functools import reduce
from operator import add
import logging
from pathlib import Path
from collections import ChainMap
from typing import Any, Union, List, Iterable, Optional, Mapping
from .config import PartialConfig

from jinja2 import Template
import yaml

from .utils import pkg_file, FileCoercible, contents_of_file_coercible


PKG_NAME = 'premark'
logger = logging.getLogger(__name__)


class Presentation:
    '''
    A RemarkJS presentation.
    '''
    markdown: str
    config: Mapping[str, Any]

    def __init__(
        self,
        markdown: FileCoercible,
        remark_args: Optional[dict[str, Union[str, bool]]] = None,
        html_template: FileCoercible = None,
        stylesheet: FileCoercible = None,
        title: Optional[str] = None,
        metafile: FileCoercible = None,
        config_file: FileCoercible = None,
    ):
        '''
        Create a new Presentation.

        Parameters
        ----------
        markdown
            The markdown from which to render the presentations. If a Path object, is
            interpreted as a file containing the markdown. If a string, is interpreted
            as the literal markdown.
        remark_args
            The arguments to pass to `remark.create` in the generated javascript.
        html_template
            The file containing HTML (and javascript) in which to insert the markdown.
        stylesheet
            The file containing CSS to include in the eventual rendered HTML.
        title
            The title of the presentation.
        metafile
            The file containing the presentation definition.
        config_file
            A yaml file containing some or all of the above config options.
        '''
        if isinstance(markdown, str):
            self.markdown = markdown
        else:
            self.markdown = contents_of_file_coercible(markdown)
        args = {
            'remark_args': remark_args,
            'html_template': html_template,
            'stylesheet': stylesheet,
            'title': title,
            'metafile': metafile
        }
        arg_config = PartialConfig({
            key: val for key, val in args.items()
            if val is not None
        })
        if config_file is not None:
            file_config = PartialConfig.from_file(config_file)
        else:
            file_config = PartialConfig({})
        default_config = PartialConfig.from_file(pkg_file('default_config.yaml'))
        # Store configs in order of priority.
        self.config = ChainMap(arg_config, file_config, default_config)

    # Provide some properties to make access of configuration easier.
    @property
    def remark_args(self) -> dict[str, Union[str, bool]]:
        return self.config['remark_args']

    @property
    def html_template(self) -> FileCoercible:
        return self.config['html_template']

    @property
    def stylesheet(self) -> FileCoercible:
        return self.config['stylesheet']

    @property
    def title(self) -> str:
        return self.config['title']

    @property
    def metafile(self) -> FileCoercible:
        return self.config['metafile']

    def to_html(self, title: str = None) -> str:
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
        template = Template(contents_of_file_coercible(self.html_template))
        stylesheet_html = f"<style>\n{self.stylesheet}\n</style>"
        return template.render(
            title=self.title,
            markdown=self.markdown,
            stylesheet=stylesheet_html,
            remark_args=self.remark_args,
        )

    def __add__(self, other: 'Presentation') -> 'Presentation':
        '''Concatenate presentations.'''
        if not isinstance(other, self.__class__):
            return NotImplemented
        html_matches = (self.html_template == other.html_template)
        style_matches = (self.stylesheet == other.stylesheet)
        remark_matches = (self.remark_args == other.remark_args)
        if html_matches and style_matches and remark_matches:
            merged_markdown = self.markdown + '\n---\n' + other.markdown
            return self.__class__(
                markdown=merged_markdown,
                **self.config
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
        metafile: str = None,
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
        raise NotImplementedError
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
