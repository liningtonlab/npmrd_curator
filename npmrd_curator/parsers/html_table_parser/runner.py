import os
import json
import re
from pathlib import Path
from typing import Dict, List, Union

import pandas as pd
import numpy as np

from . import csv_to_json, souping, parser

Pathlike = Union[Path, str]


def parse_html_str(input_html: str) -> pd.DataFrame:
    soup = parser.read_html(input_html)
    headers = parser.find_headers(soup)
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
    hspec, cspec, hmult, jcoup = parser.column_resolve(columns, ignore_cols_indices)
    cols, grid, compound_num = parser.data_to_grid(
        atom_index,
        resi=residues,
        cspec=cspec,
        hspec=hspec,
        hmult=hmult,
        hcoup=jcoup,
    )
    data = {cols[i]: g for i, g in enumerate(grid)}
    return pd.DataFrame(data), compound_num


# def parse_str(input_str: str) -> pd.DataFrame:
#     soup = souping.input_str(input_str)
#     headers = souping.soup_id_headers(soup)
#     rows = souping.soup_id_rows(soup)
#     comps = souping.soup_comp_id(soup)

#     # Used stored results from previous functions calls to run
#     compound_num = souping.compound_number(comps, headers)
#     columns = souping.get_columns(rows, headers)
#     atom_index, atom_col_index = souping.get_atom_index(columns, headers)
#     residues, residue_col_index = souping.get_residues(columns, headers)

#     # Remove atom_index_like from get_atom index
#     if atom_index is None and souping.atom_index_like(columns[0]):
#         atom_col_index, atom_index = 0, columns[0]
#         headers = ["no."] + headers
#         columns = souping.get_columns(rows, headers)

#     two_d_NMR_col_index = souping.is_2_d_nmr(headers)
#     ignore_cols = [atom_col_index] + two_d_NMR_col_index
#     if residue_col_index is not None:
#         ignore_cols.append(residue_col_index)

#     souping.fix_multidata(columns, ignore_cols)
#     float_hspec, float_cspec, hmult, jcoup, ctype = souping.column_id_cleaner_list(
#         columns, ignore_cols
#     )

#     cols, grid = souping.data_to_grid(
#         compound_num,
#         atom_index,
#         resi=residues,
#         cspec=float_cspec,
#         ctype=ctype,
#         hspec=float_hspec,
#         hmult=hmult,
#         hcoup=jcoup,
#     )
#     data = {cols[i]: g for i, g in enumerate(grid)}
#     return pd.DataFrame(data), compound_num


def convert_grid_to_json(grid_data: List[Dict], num_comp: int) -> List[Dict]:
    """Converts table to structures base dict for JSON"""
    # grid_data is already in same form as CsvReader (list of rows)
    condensed_dict = csv_to_json.csv_dict_reader_extraction(grid_data)
    csv_to_json.merge_atom_indices(condensed_dict)
    comps_data = csv_to_json.dictionary_parser(num_comp, condensed_dict)

    return csv_to_json.json_structuring(comps_data, condensed_dict)
