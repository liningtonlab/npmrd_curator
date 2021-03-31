class HtmlReadError(Exception):
    """Raised when str read into BeautifulSoup is not HTML"""

    pass


class TsvReadError(Exception):
    """Raised when str read into TSV parser invalid"""

    pass