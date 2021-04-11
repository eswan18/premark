import os
import tempfile
import filecmp

import click
from click.testing import CliRunner

from remarker import cli


def get_data_filename(filename):
    return os.path.join(os.path.dirname(__file__), "data/{0}".format(filename))


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
            output_file = tempfile.mktemp(dir=".")
            result = self.runner.invoke(
                cli.remarker,
                [
                    "-o",
                    output_file,
                    self.data_files["default_slides"],
                ],
            )
            with open(output_file, "rt") as f1, open(
                self.data_files["default_output"], "rt"
            ) as f2:
                output = f1.read()
                default_output = f2.read()
            print(output)
            print(default_output)
            assert output.strip() == default_output.strip()

    def test_cli_with_unicode_slides(self):
        with self.runner.isolated_filesystem():
            output_file = tempfile.mktemp(dir=".")
            result = self.runner.invoke(
                cli.remarker,
                [
                    "-o",
                    output_file,
                    self.data_files["unicode_slides"],
                ],
            )
            assert filecmp.cmp(output_file, self.data_files["unicode_output"])

    def test_cli_with_verbose(self):
        with self.runner.isolated_filesystem():
            output_file = tempfile.mktemp(dir=".")
            result = self.runner.invoke(
                cli.remarker,
                [
                    "--verbose",
                    "-o",
                    output_file,
                    self.data_files["default_slides"],
                ],
            )
            assert filecmp.cmp(output_file, self.data_files["default_output"])
            assert "slides_markdown_file: " in result.output
            assert "html-template: " in result.output
            assert "css-file: " in result.output
            assert "Output file: <unopened file " in result.output

    def test_cli_with_custom_css(self):
        with self.runner.isolated_filesystem():
            output_file = tempfile.mktemp(dir=".")
            result = self.runner.invoke(
                cli.remarker,
                [
                    "-o",
                    output_file,
                    "--css-file",
                    self.data_files["custom_css"],
                    "--title",
                    "testing",
                    self.data_files["default_slides"],
                ],
            )
            assert filecmp.cmp(output_file, self.data_files["with_custom_css"])
