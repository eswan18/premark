from functools import reduce
from operator import add
import logging
from pathlib import Path
from collections import ChainMap
import json
from typing import Any, Union, Iterable, Optional, Mapping

from jinja2 import Template

from .config import PartialConfig
from .section import Section
from .utils import pkg_file, FileCoercible, contents_of_file_coercible


logger = logging.getLogger(__name__)


class Presentation:
    '''
    A RemarkJS presentation.
    '''
    source: str
    markdown: str
    config: Mapping[str, Any]

    def __init__(
        self,
        source: Optional[FileCoercible] = None,
        markdown: Optional[str] = None,
        remark_args: Optional[dict[str, Union[str, bool]]] = None,
        html_template: FileCoercible = None,
        stylesheet: FileCoercible = None,
        title: Optional[str] = None,
        config_file: FileCoercible = None,
    ):
        '''
        Create a new Presentation.

        Parameters
        ----------
        source
            The file or folder containing markdown from which to render the
            presentations. If a Path object, is interpreted as a file containing the
            markdown. Cannot be passed if `markdown` is specified.
        markdown
            Literal markdown to render. Cannot be passed if `source` is specified.
        remark_args
            The arguments to pass to `remark.create` in the generated javascript.
        html_template
            The file containing HTML (and javascript) in which to insert the markdown.
        stylesheet
            The file containing CSS to include in the eventual rendered HTML.
        title
            The title of the presentation.
        config_file
            A yaml file containing some or all of the above config options.
        '''
        if (source and markdown) or (not source and not markdown):
            msg = 'Exactly one of `source` and `markdown` args must be passed.'
            raise ValueError(msg)
        args = {
            'remark_args': remark_args,
            'html_template': html_template,
            'stylesheet': stylesheet,
            'title': title,
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

        # Create or simply store the underlying markdown.
        if 'sections' in self.config:
            # Need to make sure source is path or str.
            if not isinstance(source, (str, Path)):
                cls_name = type(source).__name__
                msg = (
                    f'Unexpected type for `source` arg, got "{cls_name}" but expected '
                    'str or pathlib.Path because `sections` is specified in config'
                )
                raise TypeError(msg)
            if not Path(source).is_dir():
                msg = ('`source` arg must be a directory of markdown files if '
                       '`sections` is specified in config.')
                raise TypeError(msg)
            sections = Section.from_entries(self.config['sections'], parent_dir=source)
            self.markdown = '\n---\n'.join(s.markdown() for s in sections)
        elif source:
            try:
                self.markdown = contents_of_file_coercible(source)
            except IsADirectoryError as exc:
                msg = ('`source` arg must be a file if `sections` is not specified in '
                       'config.`')
                raise TypeError(msg) from exc
        else:
            if markdown is None:
                msg = 'If `source` arg is None, `markdown` must be specified.'
                raise ValueError(msg)
            self.markdown = markdown

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

    def to_html(self) -> str:
        '''
        Convert the presentation to HTML.

        Returns
        -------
        str
            An HTML rendering of the presentation.
        '''
        template = Template(contents_of_file_coercible(self.html_template))
        styles = contents_of_file_coercible(self.stylesheet)
        stylesheet_html = f"<style>\n{styles}\n</style>"
        remark_args = json.dumps(self.remark_args)
        return template.render(
            title=self.title,
            markdown=self.markdown,
            stylesheet=stylesheet_html,
            remark_args=remark_args,
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
