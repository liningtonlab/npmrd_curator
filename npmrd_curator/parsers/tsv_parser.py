# -*- coding: utf-8 -*-
"""
Takes TSV input from npmrd_curator app in one of two forms.
1. HTML copy pasted into Excel and then copy pasted into the webform.
2. Manually entered values in Excel.

In both cases, the inputs should be square grids (i.e. no merged cells)

In both cases there should be EXACTLY one header column, but in different formats:

1. Data names from HTML table. If there is more than one header column, 
    delete unneeded ones.
2. Each compound MUST have the following headers for every or no compounds:
    a. 1H NMR - hshift, mult, coup
    b. 13C NMR - cshift
"""
import csv
from io import StringIO
from pathlib import Path
from typing import List, Tuple, Set

import pandas as pd
from jinja2 import Template
from npmrd_curator.exceptions import TsvReadError
from npmrd_curator.parsers.html_table_parser import parse_html_str

TEMPLATE_FILE = Path(__file__).parent.joinpath("table.j2")


def render_table(thead: List[str], rows: List[List[str]]) -> str:
    template = Template(TEMPLATE_FILE.open().read())
    return template.render(thead=thead, rows=rows)


def tsv_str_ingest(input_tsv: str) -> Tuple[List[str], List[List[str]]]:
    f = StringIO(input_tsv)
    reader = csv.reader(f, delimiter="\t")
    head = next(reader)
    rows = [r for r in reader]
    return (head, rows)


def parse_tsv_str(input_tsv: str) -> Tuple[pd.DataFrame, int]:
    thead, rows = tsv_str_ingest(input_tsv)
    if len(thead) == 0 or len(rows) == 0:
        raise TsvReadError("TSV is invalid")
    # If meets manual TSV requirement
    # parse and convert to grid
    if thead[0].strip() == "atom_index":
        return parse_manual_tsv(thead, rows)
    input_html = render_table(thead, rows)
    return parse_html_str(input_html)


def parse_manual_tsv(thead: List[str], rows: List[List[str]]) -> pd.DataFrame:
    # Search for specified variables and create header and access dict
    compound_count = 1
    seen: Set[str] = set()
    for idx, h in enumerate(thead):
        if h == "atom_index":
            continue
        if h in seen:
            compound_count += 1
            seen.clear()
        seen.add(h)
        thead[idx] = f"{compound_count}_{h}"
    return pd.DataFrame.from_records(rows, columns=thead), compound_count