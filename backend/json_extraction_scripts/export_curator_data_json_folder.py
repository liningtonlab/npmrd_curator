#%%
import sys
import os
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

import importlib.metadata
rdkit_version = importlib.metadata.version("rdkit-pypi")

# Add parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from npmrd_curator.database import Submission

# setup database connection
# POSTGRES_URI should look like "postgresql://<USERNAME>:<PASSWORD>@<DB_HOST>/npmrd_curator"
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
new_npmrd_entries = sess.query(Submission).filter(Submission.handled == False).all()
# new_npmrd_entries = sess.query(Submission).filter().all()
num_new_npmd_entries = len(new_npmrd_entries)
print(f"Got {num_new_npmd_entries} new entries")
# %%

# Export JSONs for these entries to the `./submission` directory
print("Writing entries to `./export_jsons` directory")

# create directory
os.makedirs('./export_jsons', exist_ok=True)

email_replacements = {
    "tjordan@sfu.ca": "tamara_jordan@sfu.ca",
    "jtkp6n@umsystem.edu": "jtkp6n@mail.missouri.edu"
}

num_pushed=0
print_threshold = (num_new_npmd_entries // 10)
for npe in new_npmrd_entries:
    data = json.loads(npe.data)
    for curator_entry in data:
        if npe.email in email_replacements.keys():
            curator_entry['curator_email_address'] = email_replacements[npe.email]
        else:
            curator_entry['curator_email_address'] = npe.email
        curator_entry['session_uuid'] = npe.session
        curator_entry['rdkit_version'] = rdkit_version
        curator_entry['created_date'] = npe.created_date.isoformat()

    with open(f"./export_jsons/npmrd_curator_{npe.session}.json", "w") as f:
        f.write(json.dumps(data, indent=2))
        num_pushed += 1
        if num_pushed % print_threshold == 0 and num_pushed != 0:
            print(f"Completed {num_pushed / num_new_npmd_entries * 100:.0f}% of the iterations.")

print(f"finished pushing {num_new_npmd_entries} entries!")

# %%
# WARNING - MAKE SURE YOU'RE ACTUALLY SENDING THESE TO THE NP-MRD DATABASE
# Mark these now saved entries and handles
resp1 = input("Do you want to mark these entries as handled? (y/N)").lower()
if resp1 == "y":
    for npe in new_npmrd_entries:
        npe.handled = True
    sess.commit()
    sess.close()
else:
    print("Alright, the entries have been left alone in the DB")