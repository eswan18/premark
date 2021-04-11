import os
from tempfile import NamedTemporaryFile
from pathlib import Path
from typing import Union, TextIO

from click.testing import CliRunner

from remarker import cli


def get_data_filename(filename):
    return os.path.join(os.path.dirname(__file__), "data/{0}".format(filename))


def assert_same_contents(
    f1: Union[TextIO, str],
    f2: Union[TextIO, str],
    strip: bool = True,
) -> None:
    '''
    Raise AssertionError if the contents of two files aren't identical.

    Parameters
    ----------
    f1
        File-like or file path to be compared.
    f2
        File-like or file path to be compared.
    '''
    def get_contents(thing: Union[TextIO, str]) -> str:
        result: str
        if isinstance(thing, TextIO):
            result = thing.read()
        else:
            path = Path(thing)
            with open(path, 'rt') as f:
                result = f.read()
        return result

    f1_contents = get_contents(f1)
    f2_contents = get_contents(f2)
    if strip:
        f1_contents = f1_contents.strip()
        f2_contents = f2_contents.strip()
    assert f1_contents == f2_contents


class TestRemarkerCLI(object):
    def setup(self):
        self.default_slides = get_data_filename("default_slides.md")
        self.data_files = {
            "custom_css": get_data_filename("custom.css"),
            "default_output": get_data_filename("default_output.html"),
            "default_slides": get_data_filename("default_slides.md"),
            "unicode_output": get_data_filename("unicode_output.html"),
            "unicode_slides": get_data_filename("unicode_slides.md"),
            "with_custom_css": get_data_filename("with_custom_css.html"),
        }
        self.runner = CliRunner()

    def test_cli_without_arg_shows_error(self):
        result = self.runner.invoke(cli.remarker, [])
        assert result.exit_code == 2
        assert result.output.startswith("Usage: ")
        assert "Error: Missing argument" in result.output

    def test_cli_help_shows_usage(self):
        result = self.runner.invoke(cli.remarker, ["--help"])
        assert result.exit_code == 0
        assert result.output.startswith("Usage: ")

    def test_cli_with_default_css(self):
        with self.runner.isolated_filesystem():
            with NamedTemporaryFile(dir=".") as output_file:
                _ = self.runner.invoke(
                    cli.remarker,
                    [
                        "-o",
                        output_file.name,
                        self.data_files["default_slides"],
                    ],
                )
                assert_same_contents(
                    output_file.name,
                    self.data_files["default_output"]
                )

    def test_cli_with_unicode_slides(self):
        with self.runner.isolated_filesystem():
            with NamedTemporaryFile(dir=".") as output_file:
                _ = self.runner.invoke(
                    cli.remarker,
                    [
                        "-o",
                        output_file.name,
                        self.data_files["unicode_slides"],
                    ],
                )
                assert_same_contents(
                    output_file.name,
                    self.data_files["unicode_output"]
                )

    def test_cli_with_verbose(self):
        with self.runner.isolated_filesystem():
            with NamedTemporaryFile(dir=".") as output_file:
                result = self.runner.invoke(
                    cli.remarker,
                    [
                        "--verbose",
                        "-o",
                        output_file.name,
                        self.data_files["default_slides"],
                    ],
                )
                assert_same_contents(
                    output_file.name,
                    self.data_files["default_output"]
                )
                assert "slide-source: " in result.output
                assert "html-template: " in result.output
                assert "css-file: " in result.output
                assert "Output file: <unopened file " in result.output

    def test_cli_with_custom_css(self):
        with self.runner.isolated_filesystem():
            # output_file = tempfile.mktemp(dir=".")
            with NamedTemporaryFile(dir=".") as output_file:
                _ = self.runner.invoke(
                    cli.remarker,
                    [
                        "-o",
                        output_file.name,
                        "--css-file",
                        self.data_files["custom_css"],
                        "--title",
                        "testing",
                        self.data_files["default_slides"],
                    ],
                )
                assert_same_contents(
                    output_file.name,
                    self.data_files["with_custom_css"]
                )
