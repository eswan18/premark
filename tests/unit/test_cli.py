from unittest.mock import MagicMock

from click.testing import CliRunner
import pytest

from premark import cli


@pytest.fixture(scope='function')
def runner():
    return CliRunner()


def test_shows_help(runner):
    result = runner.invoke(cli.premark, [])
    assert result.exit_code == 2
    assert result.output.startswith("Usage: ")
    assert "Error: Missing argument" in result.output


def test_simple_invocation(runner, mocker):
    class PrezMock(MagicMock):
        __init__ = MagicMock(return_value=None)

        def to_html(self):
            return 'fake output'

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
