from collections import ChainMap

from premark.config import PartialConfig

def test_can_be_used_in_chain_map():
    p1 = PartialConfig({'a': 1})
    p2 = PartialConfig({'a': 2, 'b': 4, 'c': 7})
    p3 = PartialConfig({'b': 6, 'd': 8})
    chain = ChainMap(p1, p2, p3)

    assert chain['a'] == 1
    assert chain['b'] == 4
    assert chain['d'] == 8
