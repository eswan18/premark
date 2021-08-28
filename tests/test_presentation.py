import os
from collections import namedtuple
import re
from pathlib import Path

import pytest

from remarker import Presentation

DATA_DIR = Path(__file__).parent / "data"
CUSTOM_CSS = DATA_DIR / "custom.css"
DEFAULT_OUTPUT = DATA_DIR / "default_output.html"
DEFAULT_SLIDES = DATA_DIR / "default_slides.md"
UNICODE_OUTPUT = DATA_DIR / "unicode_output.html"
UNICODE_SLIDES = DATA_DIR / "unicode_slides.md"
WITH_CUSTOM_CSS = DATA_DIR / "with_custom_css.html"
SECTIONS_DIR = DATA_DIR / "sections"
SECTION_OUTPUT = DATA_DIR / "section_output.html"
ALTERNATIVE_SECTION_OUTPUT = DATA_DIR / "alternative_section_output.html"

ExamplePrez = namedtuple('ExamplePrez', 'presentation,output_html')


@pytest.fixture
def default_prez():
    return ExamplePrez(
        Presentation(DEFAULT_SLIDES),
        DEFAULT_OUTPUT
    )


@pytest.fixture
def unicode_prez():
    return ExamplePrez(
        Presentation(Path(UNICODE_SLIDES)),
        UNICODE_OUTPUT
    )

@pytest.fixture
def with_css_prez():
    return ExamplePrez(
        Presentation(
            DEFAULT_SLIDES,
            stylesheet=Path(CUSTOM_CSS),
        ),
        WITH_CUSTOM_CSS,
    )


def assert_html_equiv(s1: str, s2: str) -> None:
    whitespace = re.compile(r'\s+')
    s1 = whitespace.sub(' ', s1).strip()
    s2 = whitespace.sub(' ', s2).strip()
    try:
        assert s1 == s2
    except AssertionError:
        print(s1)
        print(s2)
        raise


### BEGIN TESTS

def test_str_and_path_md_is_same():
    p1 = Presentation(DEFAULT_SLIDES)
    with open(DEFAULT_SLIDES, 'r') as f:
        slide_md = f.read()
    p2 = Presentation(slide_md)
    assert p1 == p2


def test_default_output():
    p = Presentation(DEFAULT_SLIDES)
    actual = p.to_html()
    expected = DEFAULT_OUTPUT.read_text()
    assert_html_equiv(actual, expected)


def test_equality():
    default_prez = Presentation(DEFAULT_SLIDES)
    assert default_prez == Presentation(DEFAULT_SLIDES)
    custom_css_prez = Presentation(DEFAULT_SLIDES, stylesheet=CUSTOM_CSS)
    assert default_prez != custom_css_prez


def test_from_presentations():
    # The following relies on the sections being "supposed to be" stitched together in
    # alphabetical order.
    final = Presentation.from_presentations(
        Presentation(path) for path in SECTIONS_DIR.glob('*.md')
    )
    actual = final.to_html()
    expected = SECTION_OUTPUT.read_text()
    assert_html_equiv(actual, expected)
