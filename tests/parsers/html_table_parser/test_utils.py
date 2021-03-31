import pytest

from npmrd_curator.parsers.html_table_parser import utils
from bs4 import BeautifulSoup


def test_minify():
    inp = """
<html>
    <div>
        Test
    </div>
</html>"""
    expected = "<html><div>Test</div></html>"
    assert utils.minify(inp) == expected


def test_clean_input():
    inp = """
<html>
    <div>
        Test&nbsp;more test
    </div>
</html>"""
    expected = "<html><div>Test more test</div></html>"
    assert utils.clean_input(inp) == expected


def test_cell_clean():
    soup = BeautifulSoup("<th>Test\nCell </th>", "lxml")
    cell = soup.th
    assert utils.cell_clean(cell) == "TestCell"


def test_remove_blanks():
    inp = ["", "test1", "", "test2"]
    assert utils.remove_blanks(inp) == ["test1", "test2"]


def test_create_new_td(html_soup):
    tag = utils.create_new_td(html_soup)
    assert str(tag) == "<td></td>"