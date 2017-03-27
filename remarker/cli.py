import click
import pkg_resources
import sys
from . import presentation

DEFAULT_HTML_FILE = pkg_resources.resource_filename('remarker', 'templates/default.html')
DEFAULT_CSS_FILE = pkg_resources.resource_filename('remarker', 'templates/default.css')

def loadfile(filename):
    with open(filename) as infile:
        return infile.read()

@click.argument('slides_markdown_file', type=click.Path(exists=True))
@click.option('--html-template', type=click.Path(exists=True),
        default=DEFAULT_HTML_FILE)
@click.option('--css-file', type=click.Path(exists=True),
        default=DEFAULT_CSS_FILE)
@click.option('--output-file', '-o', type=click.File('w'), default=sys.stdout)
@click.option('--title', '-t', default='Presentation')
@click.option('--verbose', '-v', is_flag=True)
@click.command()
def remarker(slides_markdown_file, html_template, css_file, output_file,
        title, verbose):
    if verbose:
        click.echo('Input:', err=True)
        click.echo('slides_markdown_file: {}'.format(slides_markdown_file),
                err=True)
        click.echo('html-template: {}'.format(html_template), err=True)
        click.echo('css-file: {}'.format(css_file), err=True)
        click.echo('Output file: {}'.format(output_file), err=True)

    template_html = loadfile(html_template)
    slide_markdown = loadfile(slides_markdown_file)
    stylesheet_html = loadfile(css_file)

    output_html = presentation.generate_html(template_html, slide_markdown,
                stylesheet_html, title=title)
    output_file.write(output_html)

if __name__ == '__main__':
    remarker()
