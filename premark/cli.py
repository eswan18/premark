import sys
import logging
from typing import Optional, TextIO

import click

from .presentation import Presentation


logger = logging.getLogger(__name__)

DEFAULT_CONFIG_FILE = 'premark.yaml'


@click.version_option()
@click.option(
    "--stylesheet",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
    help="Custom CSS to be included inline",
)
@click.option(
    "--html",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
    help="Custom Jinja2 HTML template for the presentation",
)
@click.option("--verbose", "-v", is_flag=True, help="Output debugging info.")
@click.option("--title", "-t", help="HTML title of the presentation")
@click.option(
    "--outfile",
    "-o",
    type=click.File("wt", encoding="utf8"),
    default=sys.stdout,
    help="Write the output to a file instead of STDOUT.",
)
@click.option(
    "--config",
    "-c",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
    help="Path of Premark configuration file",
)
@click.argument(
    'source',
    type=click.Path(exists=True, file_okay=True, dir_okay=True),
)
@click.command()
def premark(
    config: Optional[str],
    source: Optional[str],
    outfile: TextIO,
    title: Optional[str],
    verbose: bool,
    html: Optional[str],
    stylesheet: Optional[str],
) -> None:
    '''
    Generate a Remark.js HTML presentation from input markdown SOURCE.
    '''
    if verbose:
        click.echo("Input:", err=True)
        click.echo("source: {}".format(source), err=True)
        click.echo("html template: {}".format(html), err=True)
        click.echo("stylesheet: {}".format(stylesheet), err=True)
        click.echo("config: {}".format(config), err=True)
        click.echo("output file: {}".format(outfile), err=True)
    logger.debug(
        'premark cli running with arguments: slide-source: %s; html-template: %s;'
        'stylesheet: %s; config: %s; output-file: %s',
        source,
        html,
        stylesheet,
        config,
        outfile,
    )
    prez = Presentation(
        source,
        html_template=html,
        stylesheet=stylesheet,
        title=title,
        config_file=config
    )
    output_html = prez.to_html()
    outfile.write(output_html)


if __name__ == "__main__":
    premark()
