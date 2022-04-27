from collections import ChainMap
from pathlib import Path

import pytest
from yaml.error import YAMLError

import premark
from premark.config import PartialConfig


def test_can_be_used_in_chain_map():
    '''
    PartialConfigs work as mappings and can be used in a ChainMap
    '''
    p1 = PartialConfig({'a': 1})
    p2 = PartialConfig({'a': 2, 'b': 4, 'c': 7})
    p3 = PartialConfig({'b': 6, 'd': 8})
    chain = ChainMap(p1, p2, p3)

    assert chain['a'] == 1
    assert chain['b'] == 4
    assert chain['d'] == 8


def test_from_file(tmp_path: Path):
    '''
    Reading from a file works as expected.
    '''
    filepath = tmp_path / 'config.yaml'
    filepath.write_text('remark_args:\n  ratio: 3\n  stuff: 7\nother: a')
    p = PartialConfig.from_file(filepath)

    assert p['other'] == 'a'
    assert p['remark_args']['ratio'] == 3


def test_from_file_fails_on_bad_yaml(tmp_path: Path):
    '''
    Invalid yaml triggers an error.
    '''
    filepath = tmp_path / 'config.yaml'
    filepath.write_text('remark_args:  ratio: 3\n  stuff: 7\nother: a')
    with pytest.raises(YAMLError):
        _ = PartialConfig.from_file(filepath)


def test_interpolates_pkg_path():
    '''
    Configs can use {{premark}} as a shorthand for the path to the package.
    '''
    p = PartialConfig({'a': 1, 'fakefile': '{{premark}}/fakefile.py'})
    expected_path = Path(premark.__file__).parent / 'fakefile.py'

    assert p['fakefile'] == str(expected_path)
