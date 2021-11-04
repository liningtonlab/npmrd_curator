import pandas as pd
import numpy as np
import pytest
from npmrd_curator.parsers import tsv_parser as tsvp
from npmrd_curator.parsers.html_table_parser import convert_grid_to_json
from pandas.testing import assert_frame_equal

## TEST DATA
TSV = """No.\t1H NMR\t13C NMR
1\t7.0-7.38\t137
2\t7.0-7.38\t129
3\t7.0-7.38\t128
4\t7.0-7.38\t125
5\t2.34\t21.4"""
THEAD = ["No.", "1H NMR", "13C NMR"]
ROWS = [
    ["1", "7.0-7.38", "137"],
    ["2", "7.0-7.38", "129"],
    ["3", "7.0-7.38", "128"],
    ["4", "7.0-7.38", "125"],
    ["5", "2.34", "21.4"],
]
EXPECTED = [
    {"atom_index": "1", "1_hshift": 7.19, "1_cshift": 137.0},
    {"atom_index": "2", "1_hshift": 7.19, "1_cshift": 129.0},
    {"atom_index": "3", "1_hshift": 7.19, "1_cshift": 128.0},
    {"atom_index": "4", "1_hshift": 7.19, "1_cshift": 125.0},
    {"atom_index": "5", "1_hshift": 2.34, "1_cshift": 21.4},
]


def test_parse_manual_tsv():
    input_tsv = """atom_index	hshift	mult	coup	hshift	mult	coup
3	8.06	s		8.06	s	
4-OCH3	4.12	d	11	4.12	d	11
5-SCH3	2.38	d	12	2.38	d	12
"""
    expected = (
        pd.DataFrame(
            [
                {
                    "atom_index": "3",
                    "1_hshift": "8.06",
                    "1_multi": "s",
                    "1_coupling": "",
                    "2_hshift": "8.06",
                    "2_multi": "s",
                    "2_coupling": "",
                },
                {
                    "atom_index": "4-OCH3",
                    "1_hshift": "4.12",
                    "1_multi": "d",
                    "1_coupling": "11",
                    "2_hshift": "4.12",
                    "2_multi": "d",
                    "2_coupling": "11",
                },
                {
                    "atom_index": "5-SCH3",
                    "1_hshift": "2.38",
                    "1_multi": "d",
                    "1_coupling": "12",
                    "2_hshift": "2.38",
                    "2_multi": "d",
                    "2_coupling": "12",
                },
            ]
        ),
        2,
    )
    output = tsvp.parse_tsv_str(input_tsv)
    print(output[1])
    print(output[0])
    # check order indifferent
    assert_frame_equal(expected[0], output[0], atol=0.1, check_like=True)
    # compound count
    assert expected[1] == output[1]


def test_parse_tsv_str():
    output = tsvp.parse_tsv_str(TSV)
    expected = (pd.DataFrame(EXPECTED), 1)
    # check order indifferent
    assert_frame_equal(expected[0], output[0], atol=0.01, check_like=True)
    # compound count
    assert expected[1] == output[1]


def test_tsv_str_ingest():
    expected = (THEAD, ROWS)
    assert expected == tsvp.tsv_str_ingest(TSV)


def test_header_lookup():
    assert tsvp.header_lookup("mult") == "multi"
    assert tsvp.header_lookup("coup") == "coupling"
    assert tsvp.header_lookup("atom_index") == "atom_index"
    assert tsvp.header_lookup("") == ""


def test_render_table():
    # toluene-ish data
    thead = ["No.", "1H NMR", "13C NMR"]
    rows = [
        ["1", "7.0-7.38", "137"],
        ["2", "7.0-7.38", "129"],
        ["3", "7.0-7.38", "128"],
        ["4", "7.0-7.38", "125"],
        ["5", "2.34", "21.4"],
    ]
    expected = """<table>
    <thead>
        <tr>
            <th>No.</th>
            <th>1H NMR</th>
            <th>13C NMR</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>1</td>
            <td>7.0-7.38</td>
            <td>137</td>
        </tr>
        <tr>
            <td>2</td>
            <td>7.0-7.38</td>
            <td>129</td>
        </tr>
        <tr>
            <td>3</td>
            <td>7.0-7.38</td>
            <td>128</td>
        </tr>
        <tr>
            <td>4</td>
            <td>7.0-7.38</td>
            <td>125</td>
        </tr>
        <tr>
            <td>5</td>
            <td>2.34</td>
            <td>21.4</td>
        </tr>
    </tbody>
</table>"""
    assert expected == tsvp.render_table(thead, rows)


def test_parse_manual_tsv_to_grid():
    input_tsv = """atom_index	hshift	mult	coup	hshift	mult	coup
3	8.06	s		8.06	s	
4-OCH3	4.12	d	11	4.12	d	11
5-SCH3	2.38	d	12	2.38	d	12
"""
    expected = [
        {
            "name": None,
            "smiles": None,
            "original_isolation": False,
            "origin_doi": None,
            "origin_type": None,
            "origin_genus": None,
            "origin_species": None,
            "c_nmr": {
                "solvent": None,
                "temperature": None,
                "reference": None,
                "frequency": None,
                "spectrum": [],
            },
            "h_nmr": {
                "solvent": None,
                "temperature": None,
                "reference": None,
                "frequency": None,
                "spectrum": [
                    {
                        "shift": 8.06,
                        "multiplicity": "s",
                        "coupling": [],
                        "lit_atom_index": "3",
                        "atom_index": "3",
                        "rdkit_index": [],
                        "interchangable_index": [],
                    },
                    {
                        "shift": 4.12,
                        "multiplicity": "d",
                        "coupling": [11.0],
                        "lit_atom_index": "4-OCH3",
                        "atom_index": "4-OCH3",
                        "rdkit_index": [],
                        "interchangable_index": [],
                    },
                    {
                        "shift": 2.38,
                        "multiplicity": "d",
                        "coupling": [12.0],
                        "lit_atom_index": "5-SCH3",
                        "atom_index": "5-SCH3",
                        "rdkit_index": [],
                        "interchangable_index": [],
                    },
                ],
            },
        },
        {
            "name": None,
            "smiles": None,
            "original_isolation": False,
            "origin_doi": None,
            "origin_type": None,
            "origin_genus": None,
            "origin_species": None,
            "c_nmr": {
                "solvent": None,
                "temperature": None,
                "reference": None,
                "frequency": None,
                "spectrum": [],
            },
            "h_nmr": {
                "solvent": None,
                "temperature": None,
                "reference": None,
                "frequency": None,
                "spectrum": [
                    {
                        "shift": 8.06,
                        "multiplicity": "s",
                        "coupling": [],
                        "lit_atom_index": "3",
                        "atom_index": "3",
                        "rdkit_index": [],
                        "interchangable_index": [],
                    },
                    {
                        "shift": 4.12,
                        "multiplicity": "d",
                        "coupling": [11.0],
                        "lit_atom_index": "4-OCH3",
                        "atom_index": "4-OCH3",
                        "rdkit_index": [],
                        "interchangable_index": [],
                    },
                    {
                        "shift": 2.38,
                        "multiplicity": "d",
                        "coupling": [12.0],
                        "lit_atom_index": "5-SCH3",
                        "atom_index": "5-SCH3",
                        "rdkit_index": [],
                        "interchangable_index": [],
                    },
                ],
            },
        },
    ]
    df, num_comp = tsvp.parse_tsv_str(input_tsv)
    json_data = convert_grid_to_json(
        df.replace({np.nan: "-"}).astype(str).to_dict(orient="records"), num_comp
    )
    assert json_data == expected