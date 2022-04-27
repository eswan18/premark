from collections import ChainMap

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

def test_from_file(tmp_path):
    '''
    Reading from a file works as expected.
    '''
    filepath = tmp_path / 'config.yaml'
    filepath.write_text('remark_args:\n  ratio: 3\n  stuff: 7\nother: a')
    c = PartialConfig.from_file(filepath)

    assert c['other'] == 'a'
    assert c['remark_args']['ratio'] == 3
