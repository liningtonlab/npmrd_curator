import pytest
import copy
from npmrd_curator.parsers.html_table_parser import csv_to_json as cj


def test_no_blank():
    assert cj.no_blank("") == False
    assert cj.no_blank("Test") == True


def test_coupling_float():
    assert cj.coupling_float("12.0") == [12.0]
    assert cj.coupling_float("12.0, 1.5") == [12.0, 1.5]
    assert cj.coupling_float("") == []


def test_multi_blank():
    assert cj.multi_blank("") == None
    assert cj.multi_blank("s") == "s"


# fmt: off
INPUT = [
    {"atom_index": "1", "1_cshift": "126.3", "1_hshift": "", "1_multi": ""},
    {"atom_index": "2", "1_cshift": "161.5", "1_hshift": "", "1_multi": ""},
    {"atom_index": "3", "1_cshift": "108.5", "1_hshift": "6.67", "1_multi": "s"},
    {"atom_index": "4", "1_cshift": "163.8", "1_hshift": "", "1_multi": ""},
    {"atom_index": "4a", "1_cshift": "108.5", "1_hshift": "", "1_multi": ""},
    {"atom_index": "5", "1_cshift": "159.1", "1_hshift": "", "1_multi": ""},
    {"atom_index": "6", "1_cshift": "107.9", "1_hshift": "6.95", "1_multi": "s"},
    {"atom_index": "7", "1_cshift": "157.1", "1_hshift": "", "1_multi": ""},
    {"atom_index": "8", "1_cshift": "149.7", "1_hshift": "", "1_multi": ""},
    {"atom_index": "8a", "1_cshift": "111.9", "1_hshift": "", "1_multi": ""},
    {"atom_index": "9", "1_cshift": "179.8", "1_hshift": "", "1_multi": ""},
    {"atom_index": "9a", "1_cshift": "130.6", "1_hshift": "", "1_multi": ""},
    {"atom_index": "10", "1_cshift": "186.6", "1_hshift": "", "1_multi": ""},
    {"atom_index": "10a", "1_cshift": "104.5", "1_hshift": "", "1_multi": ""},
    {"atom_index": "11", "1_cshift": "201.3", "1_hshift": "", "1_multi": ""},
    {"atom_index": "12", "1_cshift": "30.9", "1_hshift": "2.42", "1_multi": "s"},
    {"atom_index": "13", "1_cshift": "56.9", "1_hshift": "3.95", "1_multi": "s"},
    {"atom_index": "4-OH", "1_cshift": "", "1_hshift": "12.57", "1_multi": "s"},
    {"atom_index": "OH", "1_cshift": "", "1_hshift": "12.65", "1_multi": "s"},
    {"atom_index": "OH", "1_cshift": "", "1_hshift": "12.7", "1_multi": "s"},
]

COL_DICT = {
    "atom_index": [ "1", "2", "3", "4", "4a", "5", "6", "7", "8", "8a", "9", "9a", "10", "10a", "11", "12", "13", "4-OH", "OH", "OH", ],
    "1_cshift": [ "126.3", "161.5", "108.5", "163.8", "108.5", "159.1", "107.9", "157.1", "149.7", "111.9", "179.8", "130.6", "186.6", "104.5", "201.3", "30.9", "56.9", "", "", "", ],
    "1_hshift": [ "", "", "6.67", "", "", "", "6.95", "", "", "", "", "", "", "", "", "2.42", "3.95", "12.57", "12.65", "12.7", ],
    "1_multi": [ "", "", "s", "", "", "", "s", "", "", "", "", "", "", "", "", "s", "s", "s", "s", "s", ],
}

COL_DICT_LITAIDX = {
    "atom_index": [ "1", "2", "3", "4", "4a", "5", "6", "7", "8", "8a", "9", "9a", "10", "10a", "11", "12", "13", "4-OH", "OH", "OH", ],
    "1_cshift": [ "126.3", "161.5", "108.5", "163.8", "108.5", "159.1", "107.9", "157.1", "149.7", "111.9", "179.8", "130.6", "186.6", "104.5", "201.3", "30.9", "56.9", "", "", "", ],
    "1_hshift": [ "", "", "6.67", "", "", "", "6.95", "", "", "", "", "", "", "", "", "2.42", "3.95", "12.57", "12.65", "12.7", ],
    "1_multi": [ "", "", "s", "", "", "", "s", "", "", "", "", "", "", "", "", "s", "s", "s", "s", "s", ],
    "lit_atom_index": [ "1", "2", "3", "4", "4a", "5", "6", "7", "8", "8a", "9", "9a", "10", "10a", "11", "12", "13", "4-OH", "OH", "OH", ],
}


COMP_DICT = {
    "1": {
        "1_cshift": [ "126.3", "161.5", "108.5", "163.8", "108.5", "159.1", "107.9", "157.1", "149.7", "111.9", "179.8", "130.6", "186.6", "104.5", "201.3", "30.9", "56.9", "", "", "", ],
        "1_hshift": [ "", "", "6.67", "", "", "", "6.95", "", "", "", "", "", "", "", "", "2.42", "3.95", "12.57", "12.65", "12.7", ],
        "1_multi": [ "", "", "s", "", "", "", "s", "", "", "", "", "", "", "", "", "s", "s", "s", "s", "s", ],
    }
}
# fmt: on

OUTPUT = [
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
            "spectrum": [
                {"rdkit_index": None, "shift": 126.3, "atom_index": "1"},
                {"rdkit_index": None, "shift": 161.5, "atom_index": "2"},
                {"rdkit_index": None, "shift": 108.5, "atom_index": "3"},
                {"rdkit_index": None, "shift": 163.8, "atom_index": "4"},
                {"rdkit_index": None, "shift": 108.5, "atom_index": "4a"},
                {"rdkit_index": None, "shift": 159.1, "atom_index": "5"},
                {"rdkit_index": None, "shift": 107.9, "atom_index": "6"},
                {"rdkit_index": None, "shift": 157.1, "atom_index": "7"},
                {"rdkit_index": None, "shift": 149.7, "atom_index": "8"},
                {"rdkit_index": None, "shift": 111.9, "atom_index": "8a"},
                {"rdkit_index": None, "shift": 179.8, "atom_index": "9"},
                {"rdkit_index": None, "shift": 130.6, "atom_index": "9a"},
                {"rdkit_index": None, "shift": 186.6, "atom_index": "10"},
                {"rdkit_index": None, "shift": 104.5, "atom_index": "10a"},
                {"rdkit_index": None, "shift": 201.3, "atom_index": "11"},
                {"rdkit_index": None, "shift": 30.9, "atom_index": "12"},
                {"rdkit_index": None, "shift": 56.9, "atom_index": "13"},
            ],
        },
        "h_nmr": {
            "solvent": None,
            "temperature": None,
            "reference": None,
            "frequency": None,
            "spectrum": [
                {
                    "shift": 6.67,
                    "multiplicity": "s",
                    "coupling": [],
                    "lit_atom_index": "3",
                    "atom_index": "3",
                    "rdkit_index": [],
                    "interchangable_index": [],
                },
                {
                    "shift": 6.95,
                    "multiplicity": "s",
                    "coupling": [],
                    "lit_atom_index": "6",
                    "atom_index": "6",
                    "rdkit_index": [],
                    "interchangable_index": [],
                },
                {
                    "shift": 2.42,
                    "multiplicity": "s",
                    "coupling": [],
                    "lit_atom_index": "12",
                    "atom_index": "12",
                    "rdkit_index": [],
                    "interchangable_index": [],
                },
                {
                    "shift": 3.95,
                    "multiplicity": "s",
                    "coupling": [],
                    "lit_atom_index": "13",
                    "atom_index": "13",
                    "rdkit_index": [],
                    "interchangable_index": [],
                },
                {
                    "shift": 12.57,
                    "multiplicity": "s",
                    "coupling": [],
                    "lit_atom_index": "4-OH",
                    "atom_index": "4-OH",
                    "rdkit_index": [],
                    "interchangable_index": [],
                },
                {
                    "shift": 12.65,
                    "multiplicity": "s",
                    "coupling": [],
                    "lit_atom_index": "OH",
                    "atom_index": "OH",
                    "rdkit_index": [],
                    "interchangable_index": [],
                },
                {
                    "shift": 12.7,
                    "multiplicity": "s",
                    "coupling": [],
                    "lit_atom_index": "OH",
                    "atom_index": "OH",
                    "rdkit_index": [],
                    "interchangable_index": [],
                },
            ],
        },
    }
]


def test_listdict_to_dictlist():
    assert cj.listdict_to_dictlist(INPUT) == COL_DICT


def test_column_dict_parser():
    assert cj.column_dict_parser(1, COL_DICT) == COMP_DICT


def test_merge_atom_indices():
    assert cj.merge_atom_indices(COL_DICT) == COL_DICT_LITAIDX


def test_c_nmr_factory():
    shifts = ["", "13.0", "11.0", "2"]
    indices = ["1", "2", "3", "4"]
    expected = [
        {"rdkit_index": None, "shift": 13.0, "atom_index": "2"},
        {"rdkit_index": None, "shift": 11.0, "atom_index": "3"},
        {"rdkit_index": None, "shift": 2.0, "atom_index": "4"},
    ]
    output = cj.c_nmr_factory(shifts, indices)
    print(output)
    assert output == expected


def test_h_nmr_factory():
    indices = ["1", "2", "3", "4"]
    shifts = ["", "13.0", "11.0", "2"]
    mults = ["", "d", "s", "dd"]
    coups = ["", "1", "", "13,14"]
    expected = [
        {
            "shift": 13.0,
            "multiplicity": "d",
            "coupling": [1.0],
            "lit_atom_index": "2",
            "atom_index": "2",
            "rdkit_index": [],
            "interchangable_index": [],
        },
        {
            "shift": 11.0,
            "multiplicity": "s",
            "coupling": [],
            "lit_atom_index": "3",
            "atom_index": "3",
            "rdkit_index": [],
            "interchangable_index": [],
        },
        {
            "shift": 2.0,
            "multiplicity": "dd",
            "coupling": [13.0, 14.0],
            "lit_atom_index": "4",
            "atom_index": "4",
            "rdkit_index": [],
            "interchangable_index": [],
        },
    ]
    output = cj.h_nmr_factory(indices, indices, shifts, mults, coups)
    print(output)
    assert output == expected


def test_json_structuring():
    assert cj.json_structuring(COMP_DICT, COL_DICT_LITAIDX) == OUTPUT