#%%
import os
import sys
import json
import traceback
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime as dt

import importlib.metadata
rdkit_version = importlib.metadata.version("rdkit-pypi")

from rdkit.Chem import AllChem
from rdkit import Chem

from npmrd_curator.database import Submission
from npmrd_curator import chem


def check_for_unassigned_stereochemistry(smiles):
    mol = Chem.MolFromSmiles(smiles)
    unassigned_chiral_centers = []
    
    for atom in mol.GetAtoms():
        if atom.HasProp('_ChiralityPossible'):
            # Check if the atom's stereochemistry is unspecified
            chiral_tag = atom.GetChiralTag()
            if chiral_tag == Chem.rdchem.ChiralType.CHI_UNSPECIFIED:
                unassigned_chiral_centers.append(atom.GetIdx())
    
    return unassigned_chiral_centers


print("Connecting to DB")
POSTGRES_URI = os.getenv("POSTGRES_URI")
if POSTGRES_URI is not None:
    engine = create_engine(POSTGRES_URI)
else:
    raise ValueError("REQUIRES POSTGRES_URI")
sess: Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)()

#%%
# get all the latest data
print("Getting entries from DB")
new_npmrd_entries = sess.query(Submission).filter(Submission.id > 1271).all()
total_entries = len(new_npmrd_entries)

if len(new_npmrd_entries) == 0:
    print("no new entries to generate mol blocks for")
    sys.exit()

print(f"RUNNING FOR {total_entries} entries")

start = dt.now()

num_modified = 0
modify_max = len(new_npmrd_entries)

print_threshold = modify_max // 1

num_checked = 0
error_list = []

for npe in new_npmrd_entries:
    try:
        num_checked +=1
        data = json.loads(npe.data)

        modified = False 

        for data_entry in data:
            # Check if any unassigned stereochemistry exists (if it does then )
            unassigned_stereochemistry = check_for_unassigned_stereochemistry(data_entry['smiles'])
            
            if unassigned_stereochemistry:
                contains_unassigned_stereochemistry = True
                canonicalized_mol_block_dimensionality = "2D"
            else:
                contains_unassigned_stereochemistry = False
                canonicalized_mol_block_dimensionality = "3D"            
            
            # Only add canonicalized_mol_block if it's not already present
            if "canonicalized_mol_block" not in data_entry or data_entry["canonicalized_mol_block"] is None:
                # Generate the mol block using RDKit
                m_canon = chem.rdkit_atom_order(chem.smi_to_mol(data_entry['smiles']))
                if canonicalized_mol_block_dimensionality == "3D":
                    AllChem.EmbedMolecule(m_canon, randomSeed=0xF00D)
                data_entry['canonicalized_mol_block'] = Chem.MolToMolBlock(m_canon)
                data_entry['canonicalized_mol_block_dimensionality'] = canonicalized_mol_block_dimensionality
                data_entry['contains_unassigned_stereochemistry'] = contains_unassigned_stereochemistry
                modified = True  # Mark as modified
        
        if modified:
            num_modified += 1
            npe.data = json.dumps(data)  # Convert back to JSON and update the database field
            npe.handled = False
            
            sess.add(npe)  # Add to session to track the change
            # Commit for each entry and clear the session
            sess.commit()
            sess.expunge(npe)  # Remove the instance from the session to avoid memo
        
            # Print progress message
            # if num_modified % print_threshold == 0:
            now = dt.now()
            elapsed_so_far=now-start
            duration = ("Took: %02d:%02d:%02d:%02d" % (elapsed_so_far.days, elapsed_so_far.seconds // 3600, elapsed_so_far.seconds // 60 % 60, elapsed_so_far.seconds % 60))
            print(f"Completed {num_modified / modify_max * 100:.0f}% ({num_checked} checked, {num_modified} generated:) of conversions in {duration}.")
        
        if num_modified >= modify_max:
            break 
    
    except:
        print(traceback.format_exc())

print(f"checked {num_checked}, modified {num_modified} entries ({(num_modified/num_checked) * 100}% *) by adding mol blocks")

end = dt.now()
elapsed=end-start
duration = ("Took: %02d:%02d:%02d:%02d" % (elapsed.days, elapsed.seconds // 3600, elapsed.seconds // 60 % 60, elapsed.seconds % 60))
print(f"TOTAL - {duration}")