import re


def assert_html_equiv(s1: str, s2: str) -> None:
    whitespace = re.compile(r'\s+')
    s1 = whitespace.sub(' ', s1).strip()
    s2 = whitespace.sub(' ', s2).strip()
    assert s1 == s2
