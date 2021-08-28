from functools import reduce
from operator import add
from pathlib import Path
from typing import Optional, Union, Iterable
from pkg_resources import resource_filename

from jinja2 import Template, Environment
import yaml

DEFAULT_JAVASCRIPT = """
<script src="https://remarkjs.com/downloads/remark-latest.min.js"></script>
<script>var slideshow = remark.create({ratio: '16:9', slideNumberFormat: '(%current%/%total%)', countIncrementalSlides: false, highlightLines: true});</script>"""  # noqa
HTML_TEMPLATE = Path(resource_filename('remarker', 'templates/default.html'))
STYLESHEET = Path(resource_filename("remarker", "templates/default.css"))

# Set up the Jinja environment; otherwise newlines are stripped from rendered templates.
_env = Environment(keep_trailing_newline=True)


class Presentation:
    markdown: str
    html_template: str
    stylesheet_template: str

    def __init__(
        self,
        markdown: Union[str, Path],
        html_template: Union[str, Path] = HTML_TEMPLATE,
        stylesheet: Union[str, Path] = STYLESHEET,
    ):
        '''
        Create a new Presentation.

        Parameters
        ----------
        markdown
            The markdown from which to render the presentations. If a Path object, is
            interpreted as a file containing the markdown. If a string, is interpreted as
            the literal markdown.
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

    def to_html(self, title: str = 'Remarker Presentation') -> str:
        '''Convert the presentation to HTML.'''
        template = Template(self.html_template)
        stylesheet_html = f"<style>\n{self.stylesheet}\n</style>"
        return template.render(
            title=title,
            markdown=self.markdown,
            stylesheet=stylesheet_html,
            js=DEFAULT_JAVASCRIPT,
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

    def __eq__(self, other: 'Presentation') -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        else:
            md_matches = (self.markdown == other.markdown)
            html_matches = (self.html_template == other.html_template)
            style_matches = (self.stylesheet == other.stylesheet)
            return (md_matches and html_matches and style_matches)

    @classmethod
    def from_presentations(cls, presentations: Iterable['Presentation']) -> 'Presentation':
        '''Create a single presentations by merging others together.'''
        # Because '+' is overloaded to concatenate, this merges the inputs.
        return reduce(add, presentations)


def slides_from_path(
    source_path: Union[str, Path],
    metafile: str,
) -> str:
    '''
    Create text in markdown format for Remark to process, from a path.

    Path can be a single file or a folder. In the latter case, the folder is expected to
    contain multiple sets of slides and a slideshow.yaml file specifying the order in
    which to "stitch" the individual slideshows together.
    '''
    if not isinstance(source_path, Path):
        source_path = Path(source_path)
    if source_path.is_dir():
        metafile_path = source_path / metafile
        slide_markdown = stitch_slides(source_path, metafile_path)
    else:
        with open(source_path, 'rt') as f:
            slide_markdown = f.read()
    return slide_markdown


def stitch_slides(source_path: Path, metafile: Path) -> str:
    if not metafile.exists():
        msg = f'Expected to metafile "{metafile}"'
        raise FileNotFoundError(msg)
    with open(metafile, 'rt') as f:
        metadata = yaml.load(f, Loader=yaml.SafeLoader)
    # The file can be a list of dictionaries, or a one-entry dictionary ('sections'),
    # the value of which is a list of dictionaries
    if isinstance(metadata, dict):
        if 'sections' not in metadata:
            msg = "Expected to find 'sections' heading in metafile"
            raise ValueError(msg)
        metadata = metadata['sections']
    # If we have a list of {'file': str} pairs (vs just a list of strings), we need to
    # extract the filenames.
    if isinstance(metadata[0], dict):  # metadata is List[Dict[str, str]]
        files = [entry['file'] for entry in metadata]
    else:  # metadata is List[str]
        files = metadata
    # Check the files exist and then stitch them together.
    for fname in files:
        if not (source_path / fname).exists():
            msg = f"slide file '{fname}' not found in slide source folder"
            raise ValueError(msg)
    md = '\n---\n'.join(Path(source_path / fname).read_text() for fname in files)
    return md
