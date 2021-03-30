import os
import json
import re
from pathlib import Path
from typing import Dict, List, Union

import pandas as pd
import numpy as np

from npmrd_curator.parsers.html_table_parser import csv_to_json, parser
from npmrd_curator.exceptions import HtmlReadError

Pathlike = Union[Path, str]


def parse_html_str(input_html: str) -> pd.DataFrame:
    try:
        soup = parser.read_html(input_html)
        headers = parser.find_headers(soup)
    except AttributeError:
        raise HtmlReadError("Could not load HTML. You may be missing headers?")
    rows = parser.find_rows(soup)
    columns = parser.get_columns(rows)
    atom_index, atom_index_col_index = parser.get_atom_index(columns, headers)
    residues, residue_col_index = parser.get_residues(columns, headers)
    _2dnmr_col_indices = parser.get_2dnmr_indices(headers)
    # add indices together and remove Nones
    ignore_cols_indices = list(
        filter(
            lambda x: x is not None,
            _2dnmr_col_indices + [atom_index_col_index, residue_col_index],  # type: ignore
        )
    )
    parser.fix_multidata(columns, ignore_cols_indices)
    hshift, cshift, hmult, jcoup = parser.column_resolve(columns, ignore_cols_indices)
    cols, grid, compound_num = parser.data_to_grid(
        atom_index,
        resi=residues,
        cshift=cshift,
        hshift=hshift,
        hmult=hmult,
        hcoup=jcoup,
    )
    data = {cols[i]: g for i, g in enumerate(grid)}
    return pd.DataFrame(data), compound_num


def convert_grid_to_json(grid_data: List[Dict], num_comp: int) -> List[Dict]:
    """Converts table to structures base dict for JSON"""
    # grid_data is already in same form as CsvReader (list of rows)
    condensed_dict = csv_to_json.csv_dict_reader_extraction(grid_data)
    csv_to_json.merge_atom_indices(condensed_dict)
    comps_data = csv_to_json.dictionary_parser(num_comp, condensed_dict)

    return csv_to_json.json_structuring(comps_data, condensed_dict)
