import pytest

from npmrd_curator.parsers.html_table_parser import utils
from bs4 import BeautifulSoup


def test_remove_integration():
    s1 = "1.0 (1H, s)"
    s2 = "2.0 (2H, d, 11.0)"
    s3 = "3.0 (3H, m)"
    # These should not change
    s4 = "4.0 (3H m)"
    s5 = "5.0 (5H, m)"
    s6 = "6.0 (m)"
    assert utils.remove_integration(s1) == "1.0 (s)"
    assert utils.remove_integration(s2) == "2.0 (d, 11.0)"
    assert utils.remove_integration(s3) == "3.0 (m)"
    # These should not change
    assert utils.remove_integration(s4) == s4
    assert utils.remove_integration(s5) == s5
    assert utils.remove_integration(s6) == s6


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