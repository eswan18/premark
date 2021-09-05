import sys
import logging
from typing import Optional, TextIO
import pathlib

import click

from .presentation import Presentation, DEFAULTS

logger = logging.getLogger(__name__)


@click.argument(
    "slide-source",
    type=click.Path(exists=True, file_okay=True, dir_okay=True),
)
@click.option(
    "--html-template",
    type=click.Path(exists=True),
    help="Jinja2 template file for the presentation.",
)
@click.option(
    "--css-file",
    "-c",
    type=click.Path(exists=True),
    help="Custom CSS to be included inline.",
)
@click.option(
    "--metafile",
    "-m",
    help=("File definition for the order of section stitching. Only needed if using a "
          "sections folder.")
)
@click.option(
    "--output-file",
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
    slide_source: str,
    html_template: Optional[str],
    metafile: Optional[str],
    css_file: Optional[str],
    output_file: TextIO,
    title: Optional[str],
    verbose: bool,
) -> None:
    '''
    Generate a Remark.js HTML presentation from input Markdown and optional custom CSS.
    '''
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
