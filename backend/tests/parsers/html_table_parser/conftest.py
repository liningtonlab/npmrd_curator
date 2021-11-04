import pytest
from bs4 import BeautifulSoup
from pathlib import Path
import unicodedata


@pytest.fixture
def html_soup():
    # contents of test_1.html
    with Path(__file__).parent.joinpath("inputs", "test_1.html").open("r") as f:
        raw_html = f.read().replace("&nbsp;", " ").replace("&nbsp", " ")
    return BeautifulSoup(raw_html, "lxml")