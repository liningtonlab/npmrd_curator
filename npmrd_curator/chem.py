from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.rdDepictor import Compute2DCoords
from rdkit.Chem.Draw import rdMolDraw2D

from npmrd_curator.schemas import Format


def convert(structure: str, fmt: Format, get3d: bool) -> str:
    """Convenience function for conversion"""
    m_canon = rdkit_atom_order(smi_to_mol(structure))
    m_canon.SetProp("_Name", AllChem.CalcMolFormula(m_canon))

    if fmt == Format.sdf:
        print("SDF")
        if get3d:
            AllChem.EmbedMolecule(m_canon, randomSeed=0xF00D)
        return mol_to_sdf(m_canon) + f"\n> <SMILES>\n{structure}\n\n$$$$"
    if fmt == Format.smiles:
        print("SMILES")
        return mol_to_smi(m_canon)
    if fmt == Format.inchi:
        print("InChI")
        return mol_to_inchi(m_canon)
    if fmt == Format.svg:
        print("SVG")
        return mol_to_svg(m_canon)
    return "Broken"


def rdkit_atom_order(m, add_hs=True):
    """Canonicalize using RDKit SMILES export

    Args:
        m (rdkit.Chem.Mol): Mol object for RDKit

    Returns:
        rdkit.Chem.Mol: New canonicalized RDKit mol
    """
    m_renum = Chem.MolFromSmiles(Chem.MolToSmiles(m))
    if add_hs:
        m_canon = Chem.AddHs(m_renum)
    else:
        m_canon = m_renum
    add_atom_indices(m_canon)
    return m_canon


def add_atom_indices(mol):
    for i, a in enumerate(mol.GetAtoms()):
        a.SetAtomMapNum(i + 1)


def smi_to_mol(smi):
    return Chem.MolFromSmiles(smi)


def mol_to_smi(m):
    return Chem.MolToSmiles(m)


def mol_to_sdf(m):
    return Chem.MolToMolBlock(m)


def mol_to_inchi(m):
    return Chem.MolToInchi(m)


def mol_to_svg(m: Chem.Mol, size=(300, 300)) -> str:
    """Take SMILES and return SVG string"""
    d = rdMolDraw2D.MolDraw2DSVG(*size)
    d.drawOptions().addStereoAnnotation = True
    d.DrawMolecule(m)
    d.FinishDrawing()
    return d.GetDrawingText()
