import pytest

from npmrd_curator.parsers import textblock_writer as tw


def test_optical_rotation(sample_optical_rotations):
    for inp, out in sample_optical_rotations:
        assert tw.optical_rotation(inp) == out


def test_uv_spectroscopy(sample_uv_spectra):
    for inp, out in sample_uv_spectra:
        assert tw.uv_spectroscopy(inp) == out


def test_ir_spectroscopy(sample_ir_spectra):
    for inp, out in sample_ir_spectra:
        assert tw.ir_spectroscopy(inp) == out


def test__cnmr_shift():
    TESTS = [({"shift": 1.11, "atom_index": None}, "1.11"), ({"shift": 7}, "7.0")]
    for x in TESTS:
        assert tw._cnmr_shift(x[0]) == x[1]


def test_c_nmr(sample_cnmr_spectra):
    for inp, out in sample_cnmr_spectra:
        assert tw.c_nmr(inp) == out


def test__hnmr_shift():
    TESTS = [
        (
            {"shift": 8.78, "integration": 3, "multiplicity": "s", "coupling": [],},
            "8.78 (s, 3H)",
        ),
        (
            {"shift": 7.15, "integration": 1, "multiplicity": "d", "coupling": [8.2],},
            "7.15 (d, J = 8.2 Hz, 1H)",
        ),
        (
            {
                "shift": 2.79,
                "integration": 1,
                "multiplicity": "dt",
                "coupling": [5.5, 9.7],
            },
            "2.79 (dt, J = 5.5, 9.7 Hz, 1H)",
        ),
    ]
    for x in TESTS:
        assert tw._hnmr_shift(x[0]) == x[1]


def test_h_nmr(sample_hnmr_spectra):
    for inp, out in sample_hnmr_spectra:
        assert tw.h_nmr(inp) == out
