import sys
import pkg_resources
from typing import TextIO
import logging

import click
import codecs

from .presentation import generate_html, slides_from_path


DEFAULT_HTML_FILE = pkg_resources.resource_filename(
    "remarker", "templates/default.html"
)
DEFAULT_CSS_FILE = pkg_resources.resource_filename("remarker", "templates/default.css")
DEFAULT_SECTION_METAFILE = 'sections.yaml'


logger = logging.getLogger(__name__)


def loadfile(filename: str):
    with codecs.open(filename, encoding="utf8") as infile:
        return infile.read()


@click.argument(
    "slide-source",
    type=click.Path(exists=True, file_okay=True, dir_okay=True),
)
@click.option(
    "--html-template",
    type=click.Path(exists=True),
    default=DEFAULT_HTML_FILE,
    help="Jinja2 template file for the presentation.",
)
@click.option(
    "--css-file",
    "-c",
    type=click.Path(exists=True),
    default=DEFAULT_CSS_FILE,
    help="Custom CSS to be included inline.",
)
@click.option(
    "--section-metafile",
    "-m",
    default=DEFAULT_SECTION_METAFILE,
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
@click.option(
    "--title", "-t", default="Presentation", help="HTML title of the presentation."
)
@click.option("--verbose", "-v", is_flag=True, help="Output debugging info.")
@click.version_option()
@click.command()
def remarker(
    slide_source: str,
    html_template: str,
    section_metafile: str,
    css_file: str,
    output_file: TextIO,
    title: str,
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
    log_str = ('remarker running with arguments: slide-source: %s; html-template: %s;'
               'css-file: %s; output-file: %s')
    logger.debug(log_str, slide_source, html_template, css_file, output_file)

    template_html = loadfile(html_template)
    stylesheet_html = loadfile(css_file)

    # Users can pass a single slides markdown file or a directory of several "sections"
    # to be stitched together.
    slide_md = slides_from_path(slide_source, section_metafile)

    output_html = generate_html(
        template_html, slide_md, stylesheet_html, title=title
    )
    output_file.write(output_html)


if __name__ == "__main__":  # pragma: no cover
    remarker()
