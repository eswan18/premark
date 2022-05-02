from pathlib import Path

from premark import Presentation

from .utils.comparison import assert_html_equiv

DATA_DIR = Path(__file__).parent / "data"
SNAPSHOT_DIR = DATA_DIR / "snapshots"

DEFAULT_SLIDES_PATH = DATA_DIR / "default_slides.md"
DEFAULT_OUTPUT = SNAPSHOT_DIR / "default.html"
SECTIONS_DIR = DATA_DIR / "sections"
SECTION_OUTPUT = SNAPSHOT_DIR / "sections.html"
ALTERNATIVE_SECTION_OUTPUT = SNAPSHOT_DIR / "alternative_sections.html"
TITLED_SECTION_OUTPUT = SNAPSHOT_DIR / "titled_sections.html"
CUSTOM_CSS_PATH = DATA_DIR / "custom.css"
CUSTOM_CSS_OUTPUT = SNAPSHOT_DIR / "with_custom_css.html"


def test_default_output():
    p = Presentation(DEFAULT_SLIDES_PATH)
    actual = p.to_html()
    expected = DEFAULT_OUTPUT.read_text()
    assert_html_equiv(actual, expected)


def test_from_presentations():
    # The following relies on the sections being "supposed to be" stitched together in
    # alphabetical order.
    final = Presentation.from_presentations(
        Presentation(path) for path in SECTIONS_DIR.glob('section_*.md')
    )
    actual = final.to_html()
    expected = SECTION_OUTPUT.read_text()
    assert_html_equiv(actual, expected)


def test_multi_section():
    '''
    Multiple markdown files in a folder can be loaded as a single presentation.
    '''
    prez = Presentation(SECTIONS_DIR, config_file=SECTIONS_DIR / 'sections.yaml')
    actual = prez.to_html()
    expected = SECTION_OUTPUT.read_text()
    assert_html_equiv(actual, expected)


def test_alternative_multi_section():
    '''
    Multiple markdown files in a folder can be loaded as a single presentation.
    '''
    prez = Presentation(
        SECTIONS_DIR,
        config_file=SECTIONS_DIR / 'alternative_sections.yaml'
    )
    actual = prez.to_html()
    expected = ALTERNATIVE_SECTION_OUTPUT.read_text()
    assert_html_equiv(actual, expected)


def test_titled_multi_section():
    '''
    Premark will create title slides for sections with a title field in their config.
    '''
    prez = Presentation(
        SECTIONS_DIR,
        config_file=SECTIONS_DIR / 'titled_sections.yaml'
    )
    actual = prez.to_html()
    expected = TITLED_SECTION_OUTPUT.read_text()
    assert_html_equiv(actual, expected)


def test_with_custom_css():
    '''
    Custom CSS is inserted as expected.
    '''
    prez = Presentation(
        DEFAULT_SLIDES_PATH,
        stylesheet=CUSTOM_CSS_PATH,
        title='Check out this Style'
    )
    actual = prez.to_html()
    expected = CUSTOM_CSS_OUTPUT.read_text()
    assert_html_equiv(actual, expected)
