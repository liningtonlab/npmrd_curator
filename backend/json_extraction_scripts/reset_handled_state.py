#%%
import os
import sys
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
new_npmrd_entries = sess.query(Submission).filter(Submission.handled == True).all()
# new_npmrd_entries = sess.query(Submission).filter().all()
num_new_npmd_entries = len(new_npmrd_entries)
print(f"Got {num_new_npmd_entries} new entries")

resp1 = input("Do you want to mark all `handled` entries as `unhandled`? (y/N)").lower()
if resp1 == "y":
    for npe in new_npmrd_entries:
        npe.handled = False
    sess.commit()
    sess.close()
else:
    print("Alright, the entries have been left alone in the DB")