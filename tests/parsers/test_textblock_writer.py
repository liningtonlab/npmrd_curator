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
            {
                "shift": 8.78,
                "integration": 3,
                "multiplicity": "s",
                "coupling": [],
            },
            "8.78 (s, 3H)",
        ),
        (
            {
                "shift": 7.15,
                "integration": 1,
                "multiplicity": "d",
                "coupling": [8.2],
            },
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


def test_write_all():
    inp = {
        "name": "Compound A",
        "origin_type": None,
        "origin_genus": None,
        "origin_species": None,
        "origin_doi": None,
        "h_nmr": {
            "solvent": "DMSO-d6",
            "temperature": None,
            "reference": None,
            "frequency": None,
            "spectrum": [
                {
                    "shift": 8.78,
                    "integration": 3,
                    "multiplicity": "s",
                    "coupling": [],
                    "atom_index": None,
                    "rdkit_index": None,
                },
                {
                    "shift": 7.15,
                    "integration": 1,
                    "multiplicity": "d",
                    "coupling": [8.2],
                    "atom_index": None,
                    "rdkit_index": None,
                },
            ],
            "ambiguous": ["6−3 (br s, 5H, NH and NH2)"],
        },
        "c_nmr": {
            "solvent": "DMSO-d6",
            "temperature": None,
            "reference": None,
            "frequency": None,
            "spectrum": [
                {"shift": 175.4, "atom_index": None, "rdkit_index": None},
                {"shift": 156.5, "atom_index": None, "rdkit_index": None},
                {"shift": 147.4, "atom_index": None, "rdkit_index": None},
                {"shift": 110.5, "atom_index": None, "rdkit_index": None},
                {"shift": 52.3, "atom_index": None, "rdkit_index": None},
                {"shift": 28.8, "atom_index": None, "rdkit_index": None},
                {"shift": 28.4, "atom_index": None, "rdkit_index": None},
            ],
            "ambiguous": [],
        },
    }
    expected = "Compound A 13C NMR (DMSO-d6, δ): 175.4, 156.5, 147.4, 110.5, 52.3, 28.8, 28.4; 1H NMR (DMSO-d6, δ): 8.78 (s, 3H), 7.15 (d, J = 8.2 Hz, 1H), 6−3 (br s, 5H, NH and NH2)"
    assert expected == tw.write_all(inp)
