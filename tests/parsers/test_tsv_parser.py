import pandas as pd
import pytest
from npmrd_curator.parsers import tsv_parser as tsvp
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
