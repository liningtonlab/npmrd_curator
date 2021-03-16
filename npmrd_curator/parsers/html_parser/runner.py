import os
import re
from pathlib import Path
from typing import Dict, List

import pandas as pd

from . import csv_to_json, souping


def parse_str(input_str) -> pd.DataFrame:
    soup = souping.input_str(input_str)
    headers = souping.soup_id_headers(soup)
    rows = souping.soup_id_rows(soup)
    comps = souping.soup_comp_id(soup)

    # Used stored results from previous functions calls to run
    compound_num = souping.compound_number(comps, headers)
    columns = souping.get_columns(rows, headers)
    atom_index, atom_col_index = souping.get_atom_index(columns, headers)
    residues, residue_col_index = souping.get_residues(columns, headers)

    # Remove atom_index_like from get_atom index
    if atom_index is None and souping.atom_index_like(columns[0]):
        atom_col_index, atom_index = 0, columns[0]
        headers = ["no."] + headers
        columns = souping.get_columns(rows, headers)

    two_d_NMR_col_index = souping.is_2_d_nmr(headers)
    ignore_cols = [atom_col_index] + two_d_NMR_col_index
    if residue_col_index is not None:
        ignore_cols.append(residue_col_index)

    souping.fix_multidata(columns, ignore_cols)
    float_hspec, float_cspec, hmult, jcoup, ctype = souping.column_id_cleaner_list(
        columns, ignore_cols
    )

    cols, grid = souping.data_to_grid(
        compound_num,
        atom_index,
        resi=residues,
        cspec=float_cspec,
        ctype=ctype,
        hspec=float_hspec,
        hmult=hmult,
        hcoup=jcoup,
    )
    data = {cols[i]: g for i, g in enumerate(grid)}
    return pd.DataFrame(data), compound_num


def parse_file(path, filepath):
    inp_file = Path(path)
    out_file = Path(filepath)
    if not out_file.parent.exists():
        os.makedirs(out_file.parent)

    soup = souping.inputs(inp_file)
    headers = souping.soup_id_headers(soup)
    rows = souping.soup_id_rows(soup)
    comps = souping.soup_comp_id(soup)

    # Used stored results from previous functions calls to run
    compound_num = souping.compound_number(comps, headers)
    columns = souping.get_columns(rows, headers)
    atom_index, atom_col_index = souping.get_atom_index(columns, headers)
    residues, residue_col_index = souping.get_residues(columns, headers)

    # Remove atom_index_like from get_atom index
    if atom_index is None and souping.atom_index_like(columns[0]):
        atom_col_index, atom_index = 0, columns[0]
        headers = ["no."] + headers
        columns = souping.get_columns(rows, headers)

    two_d_NMR_col_index = souping.is_2_d_nmr(headers)
    ignore_cols = [atom_col_index] + two_d_NMR_col_index
    if residue_col_index is not None:
        ignore_cols.append(residue_col_index)

    souping.fix_multidata(columns, ignore_cols)
    float_hspec, float_cspec, hmult, jcoup, ctype = souping.column_id_cleaner_list(
        columns, ignore_cols
    )

    souping.tableto_csv(
        *souping.data_to_grid(
            compound_num,
            atom_index,
            resi=residues,
            cspec=float_cspec,
            ctype=ctype,
            hspec=float_hspec,
            hmult=hmult,
            hcoup=jcoup,
        ),
        filename=filepath
    )


def convert_csv_to_json(csvfile, outputfile, num_comp):
    """Original csv_to_json from Andrew 
    """
    csv_reader_dict = csv_to_json.input_file(csvfile)
    condensed_dict = csv_to_json.csv_dict_reader_extraction(csv_reader_dict)
    csv_to_json.merge_atom_indices(condensed_dict)
    comps_data = csv_to_json.dictionary_parser(num_comp, condensed_dict)
    json_structured_output = csv_to_json.json_structuring(comps_data, condensed_dict)
    csv_to_json.json_dump(json_structured_output, outputfile)


def convert_grid_to_json(grid_data: List[Dict], num_comp: int) -> List[Dict]:
    """grid_data is already in same form as CsvReader (list of rows)
    """
    condensed_dict = csv_to_json.csv_dict_reader_extraction(grid_data)
    csv_to_json.merge_atom_indices(condensed_dict)
    comps_data = csv_to_json.dictionary_parser(num_comp, condensed_dict)

    return csv_to_json.json_structuring(comps_data, condensed_dict)
