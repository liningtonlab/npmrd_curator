# -*- coding: utf-8 -*-
import pytest

import pandas as pd
from pandas.testing import assert_frame_equal
from pathlib import Path
from nmr_html_parser import runner
from nmr_html_parser import column_test
from bs4 import BeautifulSoup

# Add some real unit tests
TESTDIR = Path(__file__).parent

# disables autoformatting
# fmt: off
FILES_RESULTS = [("test_1", [['2', '', '3a', '4', '4a', '5', '7a', '8', '8a', '9', '10', '11', '12', '12a', '12b', '12c', '12d', '1′', '', '2′', 'NH', '', 'OMe-9', 'OMe-11', 'OMe-12'], ['102.5, CH2', '', '153.9, C', '105.4, CH', '118.6, C', '163.4, C', '152.3, C', '39.0, CH', '121.0, C', '150.5, C', '113.2, CH', '113.1, CH', '151.5, C', '118.0, C', '111.7, C', '150.6, C', '119.7, C', '34.7, CH2', '', '170.4, C', '', '', '56.6, CH3', '', '56.3, CH3'], ['6.21, d (0.9)', '6.35, d (0.9)', '', '7.59, s', '', '', '', '5.48, s', '', '', '7.03, d (9.2)', '7.02, d (9.2)', '', '', '', '', '', '3.09, d (16.9)', '3.48, d (16.9)', '', '5.69, br s', '6.96, br s', '3.95, s', '', '3.89, s'], ['103.1, CH2', '', '153.4, C', '106.4, CH', '119.2, C', '163.3, C', '152.0, C', '38.7, CH', '111.9, C', '157.7, C', '99.8, CH', '161.4, C', '104.5, CH', '128.9, C', '114.9, C', '149.8, C', '118.2, C', '34.3, CH2', '', '170.6, C', '', '', '56.2, CH3', '55.6, CH3', ''], ['6.30, d (0.9)', '6.42, d (0.9)', '', '7.65, s', '', '', '', '5.47, s', '', '', '6.59, d (2.3)', '', '7.54, d (2.3)', '', '', '', '', '3.08, d (16.9)', '3.59, d (16.9)', '', '5.55, br s', '6.95, br s', '3.97, s', '3.89, s', '']]
)]

# fmt: on
FILES = sorted(
    [
        "test_error_characters_ab_2",
        "test_error_characters_ab_3",
        "test_error_characters_axeq_3",
        "test_error_characters_c_2",
        "test_error_characters_h_1",
        "test_error_characters_noai_1",
        "test_error_characters_noai_2",
        "test_JOC_1",
        "test_JOC_2",
        "test_JOC_3",
        "test_JOL_1",
        "test_JOL_2",
        "test_JOL_3",
        "test_mult_ai_1",
        "test_mult_aiwres",
        "test_mult_aiwres_2",
        "test_multi_data_dash_2",
        "test_multi_data_semi_1",
        "test_oneline",
        "test_other_mult_1",
        "test_residue_4_2DNMR",
        "test_residue_3",
        "test_residue_1",
        "test_rowspan2_3",
        "test_rowspan2_2",
        "test_rowspan2_1",
        "test_semi_coup",
        "test_1",
        "test_2",
        "test_2DNMR",
        "test_3",
        "test_4",
        "test_5_c",
        "test_5_h",
        "test_6_c",
        "test_6_h_overlapped",
        "test_7_c",
        "test_8_c",
        "test_8_h",
        "test_9",
        "test_10",
        "test_11",
        "test_12",
        "test_13",
        "test_14",
        "test_15",
        "test_16",
        "test_17",
        "test_18",
        "test_19",
        "test_20",
        "test_atag_1",
        "test_atag_2",
        "test_atag_3",
        "test_atag_4",
        "test_atag_5",
        "test_atag_6",
        "test_Both_no_CHn",
        "test_CNMR_no_headers",
        "test_CNMR_number_headers",
        "test_CNMR_ONLY",
        "test_multi_h_semi",
        "test_multi_h_space",
        "test_ND_1",
        "test_ND_2",
        "test_ND_3",
        "test_ND_4",
        "test_ND_5",
        "test_negative_shift",
        "test_v1f_1",
        "test_v1f_2",
        "test_v1f_3",
        "test_v1f_4",
        "test_v1f_5",
        "test_v1f_6",
        "test_v1f_7",
        "test_v1f_8",
        "test_v1f_9",
        "test_v1f_10",
        "test_v1f_11",
        "test_v1f_12",
        "test_v1f_13",
        "test_v1f_14",
        "test_v1f_15",
        "test_v1f_16",
        "test_v1f_17",
        "test_v1f_18",
        "test_v1f_19",
        "test_v1f_20",
        "test_v1f_21",
        "test_v1f_22",
        "test_v1f_23",
        "test_v1f_24",
        "test_v1f_25",
        "test_v1f_26",
        "test_v1f_27",
        "test_v1f_28",
        "test_v1f_29",
        "test_v1f_30",
        "test_v1f_31",
        "test_v1f_32",
        "test_v1f_33",
    ]
)


def load_expected(fname):
    fpath = TESTDIR / "outputs" / fname
    return pd.read_csv(fpath)


@pytest.mark.parametrize("fname", FILES)
def test_parse(fname):
    print(fname)
    filepath = Path() / "test_outputs" / f"{fname}.csv"
    expected = load_expected(f"{fname}.csv")
    runner.parse_file(TESTDIR / "inputs" / f"{fname}.html", filepath)
    output = pd.read_csv(filepath)
    print(expected, output)
    assert_frame_equal(expected, output)


# Useless as using list with parametrize
# def load_columns(fname):
# fpath = TESTDIR / "column_outputs" / fname
# inp_file1 = Path(fpath)
# with inp_file1.open() as f:
#  f = f.read()
#  f = str(f).replace("&nbsp;", " ")
#  f = f.encode("cp1252")
#  soup = BeautifulSoup(f, "lxml")
# return soup.get_text()


@pytest.mark.parametrize("fname, expected", FILES_RESULTS)
def test_columns(fname, expected):
    # take file with expected columns results
    filepath = Path() / "test_outputs" / f"{fname}.txt"
    # run input file, and create column
    output = column_test.column(TESTDIR / "inputs" / f"{fname}.html", filepath)
    # Run assertions to check if output matches expected
    assert expected == output


# def test_inputs():
#     # Need to make this better
#     soup = souping.inputs(TESTDIR / "test_table.html")
#     assert isinstance(soup, BeautifulSoup)
#     assert soup.prettify()
#     # This next line causes test to fail on purpose as a demonstration
#     # assert False
