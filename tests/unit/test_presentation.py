from pathlib import Path

from premark import Presentation


DATA_DIR = Path(__file__).parent.parent / "data"
CUSTOM_CSS = DATA_DIR / "custom.css"
DEFAULT_SLIDES_PATH = DATA_DIR / "default_slides.md"
WITH_CUSTOM_CSS = DATA_DIR / "with_custom_css.html"


def test_str_and_path_md_is_same():
    p1 = Presentation(DEFAULT_SLIDES_PATH)
    with open(DEFAULT_SLIDES_PATH, 'r') as f:
        slide_md = f.read()
    p2 = Presentation(markdown=slide_md)
    assert p1 == p2


def test_equality():
    default_prez = Presentation(DEFAULT_SLIDES_PATH)
    assert default_prez == Presentation(DEFAULT_SLIDES_PATH)
    custom_css_prez = Presentation(DEFAULT_SLIDES_PATH, stylesheet=CUSTOM_CSS)
    assert default_prez != custom_css_prez
