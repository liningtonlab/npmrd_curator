import pytest


@pytest.fixture
def sample_optical_rotations():
    return [
        (
            {
                "temperature": 20,
                "reference": "D",
                "value": 25.4,
                "concentration": 1.00,
                "solvent": "CHCl3",
            },
            "[α]20D +25.4 (c 1.00, CHCl3)",
        ),
        (
            {
                "temperature": 27,
                "reference": "D",
                "value": -177.7,
                "concentration": 1.02,
                "solvent": "CHCl3",
            },
            "[α]27D -177.7 (c 1.02, CHCl3)",
        ),
        ({}, ""),
    ]


@pytest.fixture
def sample_uv_spectra():
    return [
        (
            {
                "solvent": "CH3OH",
                "units": "nm",
                "spectrum": [
                    {"wavelength": 210, "absorptivity": 3.33},
                    {"wavelength": 242, "absorptivity": 3.02},
                    {"wavelength": 288, "absorptivity": 2.21},
                    {"wavelength": 421, "absorptivity": 3.16},
                ],
            },
            "UV (CH3OH) λmax, nm (log ε) 210 (3.33), 242 (3.02), 288 (2.21), 421 (3.16)",
        ),
        (
            {
                "solvent": "hexanes",
                "units": "nm",
                "spectrum": [{"wavelength": 250, "absorptivity": 1070},],
            },
            "UV (hexanes) λmax, nm (ε) 250 (1070)",
        ),
        ({}, ""),
    ]


@pytest.fixture
def sample_ir_spectra():
    return [
        (
            {
                "solvent": "KBr, thin film",
                "units": "cm-1",
                "spectrum": [3017, 2953, 2855, 2192, 1512, 1360, 1082, 887],
            },
            "IR (KBr, thin film) (cm-1) 3017, 2953, 2855, 2192, 1512, 1360, 1082, 887",
        ),
        ({}, ""),
    ]


@pytest.fixture
def sample_cnmr_spectra():
    return [
        (
            {
                "solvent": "DMSO-d6",
                "temperature": None,
                "reference": None,
                "frequency": None,
                "spectrum": [
                    {"shift": 175.4, "atom_index": None, "rdkit_index": None},
                    {"shift": 156.5, "atom_index": None, "rdkit_index": None},
                    {"shift": 147.4, "atom_index": None, "rdkit_index": None},
                    {"shift": 138.3, "atom_index": None, "rdkit_index": None},
                    {"shift": 110.5, "atom_index": None, "rdkit_index": None},
                    {"shift": 52.3, "atom_index": None, "rdkit_index": None},
                    {"shift": 28.8, "atom_index": None, "rdkit_index": None},
                    {"shift": 28.4, "atom_index": None, "rdkit_index": None},
                ],
                "ambiguous": [],
            },
            "13C NMR (DMSO-d6, δ): 175.4, 156.5, 147.4, 138.3, 110.5, 52.3, 28.8, 28.4",
        ),
        (
            {
                "solvent": "CDCl3",
                "temperature": None,
                "reference": None,
                "frequency": "151 MHz",
                "spectrum": [
                    {"shift": 168.9, "atom_index": None, "rdkit_index": None},
                    {"shift": 165.4, "atom_index": None, "rdkit_index": None},
                    {"shift": 110.3, "atom_index": None, "rdkit_index": None},
                    {"shift": 69.7, "atom_index": None, "rdkit_index": None},
                    {"shift": 69.4, "atom_index": None, "rdkit_index": None},
                    {"shift": 64.6, "atom_index": None, "rdkit_index": None},
                    {"shift": 38.5, "atom_index": None, "rdkit_index": None},
                    {"shift": 30.4, "atom_index": None, "rdkit_index": None},
                    {"shift": 30.3, "atom_index": None, "rdkit_index": None},
                    {"shift": 28.6, "atom_index": None, "rdkit_index": None},
                    {"shift": 25.4, "atom_index": None, "rdkit_index": None},
                    {"shift": 22.3, "atom_index": None, "rdkit_index": None},
                    {"shift": 14.2, "atom_index": None, "rdkit_index": None},
                    {"shift": 13.9, "atom_index": None, "rdkit_index": None},
                ],
                "ambiguous": ["29.8–29.2 (11C)"],
            },
            "13C NMR (151 MHz, CDCl3, δ): 168.9, 165.4, 110.3, 69.7, 69.4, 64.6, 38.5, 30.4, 30.3, 28.6, 25.4, 22.3, 14.2, 13.9, 29.8–29.2 (11C)",
        ),
        ({}, ""),
    ]


@pytest.fixture
def sample_hnmr_spectra():
    return [
        (
            {
                "solvent": "CD3OD",
                "temperature": None,
                "reference": None,
                "frequency": "400 MHz",
                "spectrum": [
                    {
                        "shift": 8.73,
                        "integration": 3,
                        "multiplicity": "s",
                        "coupling": [],
                    },
                    {
                        "shift": 7.50,
                        "integration": 1,
                        "multiplicity": "s",
                        "coupling": [],
                    },
                    {
                        "shift": 7.15,
                        "integration": 1,
                        "multiplicity": "d",
                        "coupling": [8.2],
                    },
                ],
                "ambiguous": ["6−3 (br s, 5H, NH and NH2)"],
            },
            "1H NMR (400 MHz, CD3OD, δ): 8.73 (s, 3H), 7.50 (s, 1H), 7.15 (d, J = 8.2 Hz, 1H), 6−3 (br s, 5H, NH and NH2)",
        ),
        (
            {
                "solvent": "CDCl3",
                "temperature": None,
                "reference": None,
                "frequency": "500 MHz",
                "spectrum": [
                    {
                        "shift": 1.12,
                        "integration": 3,
                        "multiplicity": "t",
                        "coupling": [7.1],
                    },
                    {
                        "shift": 3.34,
                        "integration": 2,
                        "multiplicity": "q",
                        "coupling": [7.1],
                    },
                    {
                        "shift": 3.38,
                        "integration": 2,
                        "multiplicity": "t",
                        "coupling": [6.0],
                    },
                    {
                        "shift": 3.72,
                        "integration": 2,
                        "multiplicity": "t",
                        "coupling": [6.0],
                    },
                    {
                        "shift": 6.57,
                        "integration": 2,
                        "multiplicity": "dd",
                        "coupling": [8.7],
                    },
                ],
                "ambiguous": [],
            },
            "1H NMR (500 MHz, CDCl3, δ): 1.12 (t, J = 7.1 Hz, 3H), 3.34 (q, J = 7.1 Hz, 2H), 3.38 (t, J = 6.0 Hz, 2H), 3.72 (t, J = 6.0 Hz, 2H), 6.57 (dd, J = 8.7 Hz, 2H)",
        ),
        ({}, ""),
    ]
