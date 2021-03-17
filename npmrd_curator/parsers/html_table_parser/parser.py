from bs4 import BeautifulSoup


def read_html(input_str: str) -> BeautifulSoup:
    """Takes str, does cleaning as input and returns BeautifulSoup object"""
    f = _clean_input(input_str)
    soup = BeautifulSoup(f, "lxml")
    # removes all links
    [soup.a.decompose() for _ in soup.find_all("a")]
    return soup


def _clean_input(input_str: str) -> str:
    f = _minify(input_str)
    for schar in ["&nbsp;", "&nbsp"]:
        f = f.replace(schar, " ")
    return f


def _minify(input_str: str) -> str:
    return "".join([x.strip() for x in input_str.split("\n")])