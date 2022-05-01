from unittest.mock import MagicMock

from click.testing import CliRunner
import pytest

from premark import cli


@pytest.fixture(scope='function')
def runner():
    return CliRunner()


@pytest.fixture
def PrezMock():
    '''
    Mock Presentation class.
    '''
    class _PrezMock(MagicMock):
        __init__ = MagicMock(return_value=None)

        def to_html(self):
            return 'fake output'

    return _PrezMock


def test_shows_help(runner):
    result = runner.invoke(cli.premark, [])
    assert result.exit_code == 2
    assert result.output.startswith("Usage: ")
    assert "Error: Missing argument" in result.output


def test_simple_invocation(runner, mocker, PrezMock):
    '''
    A simple call to the CLI passes the expected args to Presentation.
    '''
    mocker.patch('premark.cli.Presentation', PrezMock)
    source_file = 'slides.md'
    out_file = 'slides.html'

    with runner.isolated_filesystem():
        with open(source_file, 'wt') as f:
            f.write('# Slide 1\n---')
        result = runner.invoke(cli.premark, ['-o', out_file, source_file])
        # The output file should contain the result of to_html()
        with open(out_file, 'rt') as f:
            assert f.read() == 'fake output'

    assert result.exit_code == 0
    PrezMock.__init__.assert_called_once_with(
        source_file,
        html_template=None,
        stylesheet=None,
        title=None,
        config_file=None,
    )


def test_full_invocation(runner, mocker, PrezMock):
    '''
    A complex call to the CLI passes the expected args to Presentation.
    '''
    mocker.patch('premark.cli.Presentation', PrezMock)
    source_file = 'slides.md'
    html_file = 'template.html'
    css_file = 'styles.css'
    config_file = 'config.yaml'
    out_file = 'slides.html'
    title = 'My Prez'

    with runner.isolated_filesystem():
        for filename in (source_file, html_file, css_file, config_file):
            with open(filename, 'wt') as f:
                f.write('Nonsense')
        result = runner.invoke(cli.premark, [
            '--outfile', out_file,
            '--html', html_file,
            '--stylesheet', css_file,
            '--title', title,
            '--config', config_file,
            source_file
        ])
        # The output file should contain the result of to_html()
        with open(out_file, 'rt') as f:
            assert f.read() == 'fake output'

    assert result.exit_code == 0
    PrezMock.__init__.assert_called_once_with(
        source_file,
        html_template=html_file,
        stylesheet=css_file,
        title=title,
        config_file=config_file,
    )
