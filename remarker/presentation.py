from pathlib import Path
from typing import Optional, Union
import logging
import json

from jinja2 import Template
import yaml


try:
    import importlib.resources as resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as resources  # type: ignore

config_contents = resources.read_text(__package__, 'config.yaml')
config = yaml.load(config_contents, Loader=yaml.SafeLoader)
remark_args = config['remark_args']

default_javascript = f"""
    <script src="https://remarkjs.com/downloads/remark-latest.min.js"></script>
    <script>var slideshow = remark.create({json.dumps(remark_args)});</script>"""

logger = logging.getLogger(__name__)


def generate_html(
    template_html: str,
    slide_markdown: str,
    stylesheet_html: str,
    title: Optional[str] = None,
):
    '''
    Generate HTML of a Reveal.js presentation.
    '''

    stylesheet_html = "<style>\n{0}</style".format(stylesheet_html)
    presentation = {
        "stylesheet_html": stylesheet_html,
        "slide_source": slide_markdown,
        "title": title,
    }
    remark = {
        "javascript": default_javascript,
    }
    template = Template(template_html)
    return template.render(
        presentation=presentation,
        remark=remark
    )


def slides_from_path(
    source_path: Union[str, Path],
    metafile: str,
) -> str:
    '''
    Create text in markdown format for Remark to process, from a path.

    Path can be a single file or a folder. In the latter case, the folder is expected to
    contain multiple sets of slides and a metafile specifying the order in which to
    "stitch" the individual slideshows together.
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
    '''
    Assemble multiple markdown files into a single one for Remark to process.

    Metafile must define an order in which the files should be assembled.
    '''
    if not metafile.exists():
        msg = f'Expected to metafile "{metafile}"'
        raise FileNotFoundError(msg)
    with open(metafile, 'rt') as f:
        metadata = yaml.load(f, Loader=yaml.SafeLoader)
    # The file can be a list of dictionaries, or a one-entry dictionary ('sections'),
    # the value of which is a list of dictionaries.
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
    logger.info('Markdown files: %s', files)
    # Check the files exist and then stitch them together.
    for i, fname in enumerate(files):
        # If the filename has no suffix, assume it's .md
        if '.' not in fname:
            fname = f'{fname}.md'
            files[i] = fname
            logger.info(f'Inferring .md suffix: changing {fname} to {fname}.md')
        if not (source_path / fname).exists():
            msg = f"slide file '{fname}' not found in slide source folder"
            raise ValueError(msg)
    md = '\n---\n'.join(Path(source_path / fname).read_text() for fname in files)
    return md
