import click
import filecmp
import os
from click.testing import CliRunner
from remarker import cli


def get_data_filename(filename):
    return os.path.join(os.path.dirname(__file__), 'data/{0}'.format(filename))


class TestRemarkerCLI(object):

    def setup(self):
        self.default_slides = get_data_filename('default_slides.md')
        self.data_files = {
                'custom_css': get_data_filename('custom.css'),
                'default_output': get_data_filename('default_output.html'),
                'default_slides': get_data_filename('default_slides.md'),
                'with_custom_css': get_data_filename('with_custom_css.html'),
                }
        self.runner = CliRunner()

    def test_cli_without_arg_shows_error(self):
        result = self.runner.invoke(cli.remarker, [])
        assert result.exit_code == 2
        assert 'Error: Missing argument "slides_markdown_file".' in result.output

    def test_cli_help_shows_usage(self):
        result = self.runner.invoke(cli.remarker, ['--help'])
        assert result.exit_code == 0
        assert 'Usage: remarker [OPTIONS] SLIDES_MARKDOWN_FILE' in result.output

    def test_cli_with_default_css(self):
        with self.runner.isolated_filesystem():
            result = self.runner.invoke(cli.remarker, ['-o',
                'test_output.html', self.data_files['default_slides'],])
            assert filecmp.cmp('test_output.html', self.data_files['default_output'])

    def test_cli_with_custom_css(self):
        with self.runner.isolated_filesystem():
            result = self.runner.invoke(cli.remarker, ['-o',
                'test_output.html', '--css-file', self.data_files['custom_css'],
                '--title', 'testing',
                self.data_files['default_slides'],])
            assert filecmp.cmp('test_output.html', self.data_files['with_custom_css'])
