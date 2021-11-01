import sys
import logging
from typing import Optional, TextIO
import pathlib

import click

from .presentation import Presentation
from .configuration import get_config_from_file, get_config_from_dict, CONFIG_DEFAULTS

logger = logging.getLogger(__name__)

DEFAULT_CONFIG_FILE = 'premark.yaml'


@click.option(
    "--source",
    type=click.Path(exists=True, file_okay=True, dir_okay=True),
    help="Path of source markdown file or folder",
)
@click.option(
    "--config",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
    help="Path of Premark configuration file",
)
@click.option(
    "--html",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
    help="Jinja2 template file for the presentation.",
)
@click.option(
    "--js",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
    help="Javascript to be embedded in the HTML template",
)
@click.option(
    "--css",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
    help="Custom CSS to be included inline.",
)
@click.option(
    "--outfile",
    "-o",
    type=click.File("wt", encoding="utf8"),
    default=sys.stdout,
    help="Write the output to a file instead of STDOUT.",
)
@click.option("--title", "-t", help="HTML title of the presentation.")
@click.option("--verbose", "-v", is_flag=True, help="Output debugging info.")
@click.version_option()
@click.command()
def premark(
    config: Optional[str],
    source: Optional[str],
    html: Optional[str],
    js: Optional[str],
    css: Optional[str],
    outfile: TextIO,
    title: Optional[str],
    verbose: bool,
) -> None:
    '''
    Generate a Remark.js HTML presentation from input markdown.
    '''
    return
    if verbose:
        click.echo("Input:", err=True)
        click.echo("slide-source: {}".format(slide_source), err=True)
        click.echo("html-template: {}".format(html_template), err=True)
        click.echo("css-file: {}".format(css_file), err=True)
        click.echo("Output file: {}".format(output_file), err=True)
    log_str = ('premark running with arguments: slide-source: %s; html-template: %s;'
               'css-file: %s; output-file: %s')
    logger.debug(log_str, slide_source, html_template, css_file, output_file)

    # Users can pass a single slides markdown file or a directory of several "sections"
    # to be stitched together.
    slide_source_path = pathlib.Path(slide_source)
    if slide_source_path.is_dir():
        if css_file or html_template or title:
            msg = ('If `slide-source` is a directory, none of `css_file`, '
                   '`html_template`, or `title` may be specified')
            raise click.ClickException(msg)
        metafile = metafile or DEFAULTS.metafile
        p = Presentation.from_directory(slide_source_path, metafile)
    else:
        if metafile:
            msg = 'If `slide-source` is a file, `metafile` may not be specified'
            raise click.ClickException(msg)
        if html_template:
            html_template_path = pathlib.Path(html_template)
        else:
            html_template_path = DEFAULTS.html_template
        if css_file:
            css_file_path = pathlib.Path(css_file)
        else:
            css_file_path = DEFAULTS.stylesheet
        p = Presentation(
            slide_source_path,
            html_template=html_template_path,
            stylesheet=css_file_path
        )

    title = title or DEFAULTS.title
    output_html = p.to_html(title=title)
    output_file.write(output_html)


if __name__ == "__main__":  # pragma: no cover
    premark()
