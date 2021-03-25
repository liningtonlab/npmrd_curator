# -*- coding: utf-8 -*-

import tempfile
from pathlib import Path

import pandas as pd
import pytest
from bs4 import BeautifulSoup
from npmrd_curator.parsers.html_table_parser import parser, runner
from pandas.testing import assert_frame_equal


def test_read_html():
    inp = """
<html>
    <div>
        <a href="#">1</a>Test&nbsp;more test<a href="#">3</a>
    </div>
</html>"""
    expected = "<html><body><div>Test more test</div></body></html>"
    output = parser.read_html(inp)
    assert isinstance(output, BeautifulSoup)
    assert str(output) == expected
    assert not output.find_all("a")


def test_find_headers(html_soup):
    expected = ["no.", "δC, type", "δH (J in Hz)", "δC, type", "δH (J in Hz)"]
    headers = parser.find_headers(html_soup)
    assert headers == expected


def test_find_rows(html_soup):
    rows = parser.find_rows(html_soup)
    assert len(rows) == 25
    assert rows[0] == [
        "2",
        "102.5, CH2",
        "6.21, d (0.9)",
        "103.1, CH2",
        "6.30, d (0.9)",
    ]


def test_find_compound_ids(html_soup):
    compound_ids = parser.find_compound_ids(html_soup)
    assert len(compound_ids) == 2
    assert compound_ids == ["1", "2"]


def test_detect_number_compounds(html_soup):
    compound_ids = parser.find_compound_ids(html_soup)
    headers = parser.find_headers(html_soup)
    num_compounds = parser.detect_number_compounds(compound_ids, headers)
    assert num_compounds == 2


def test_get_columns():
    rows = [
        ["1", "2", "3", "4"],
        ["1", "2", "3", "4"],
        ["1", "2", "3", "4"],
        ["1", "2", "3", "4"],
    ]
    expected = [
        ["1", "1", "1", "1"],
        ["2", "2", "2", "2"],
        ["3", "3", "3", "3"],
        ["4", "4", "4", "4"],
    ]
    assert parser.get_columns(rows) == expected


# Add some real unit tests
TESTDIR = Path(__file__).parent

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
    expected = load_expected(f"{fname}.csv")
    with open(TESTDIR / "inputs" / f"{fname}.html") as f:
        html_input = f.read()
    df, _ = runner.parse_html_str(html_input)
    # hack needed or else dtypes are all over the place...
    with tempfile.NamedTemporaryFile() as temp:
        df.to_csv(temp.name, index=False)
        output = pd.read_csv(temp.name)
    print(expected, output)
    assert_frame_equal(expected, output, atol=0.01)
