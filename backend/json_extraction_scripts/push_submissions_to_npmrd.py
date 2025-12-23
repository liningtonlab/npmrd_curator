# push_submissions_to_npmrd.py
"""
This is a band-aid function designed to push data from the curator that Jeff built without actually having
to go in and change anything about it.

Pushes data to NP-MRD prod endpoint AND 

"""


import sys
import os
import json
import requests
import boto3
import traceback
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

import importlib.metadata
rdkit_version = importlib.metadata.version("rdkit-pypi")

# Add parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from npmrd_curator.database import Submission

# -------------------------
# SETTINGS
# -------------------------
POSTGRES_URI = os.getenv("POSTGRES_URI")
ENDPOINT_URL = "https://npdeposition.org/api/back/npmrd_exchange/ingest_curator_json_list"
NP_DEPOSITION_API_BEARER_TOKEN = os.getenv("NP_DEPOSITION_API_BEARER_TOKEN")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
ARCHIVE_S3_BUCKET_NAME = os.getenv("ARCHIVE_S3_BUCKET_NAME")
MAX_ENTRIES_TO_PUSH = 4  # set a cap for testing or batch sending
EXPORT_JSON_DIR = "./export_jsons"  # temporary local folder
# -------------------------

# Setup DB connection
print("Connecting to DB")
if POSTGRES_URI is not None:
    engine = create_engine(POSTGRES_URI)
else:
    raise ValueError("REQUIRES POSTGRES_URI")
sess: Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)()

# Setup S3 client
s3 = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

# Ensure local export dir exists
os.makedirs(EXPORT_JSON_DIR, exist_ok=True)

#%%
# get unhandled entries
print("Getting entries from DB")
new_npmrd_entries = sess.query(Submission).filter(Submission.handled == False).all()
num_new_npmd_entries = len(new_npmrd_entries)
print(f"Got {num_new_npmd_entries} new entries")

if MAX_ENTRIES_TO_PUSH:
    new_npmrd_entries = new_npmrd_entries[:MAX_ENTRIES_TO_PUSH]

#%%
# Email replacements
email_replacements = {
    "tjordan@sfu.ca": "tamara_jordan@sfu.ca",
    "jtkp6n@umsystem.edu": "jtkp6n@mail.missouri.edu"
}

num_pushed = 0
print_threshold = max(len(new_npmrd_entries) // 10, 1)

for npe in new_npmrd_entries:
    data = json.loads(npe.data)

    # Skip entry if any curator_entry doesn't have canonicalized_mol_block
    if any('canonicalized_mol_block' not in entry or entry['canonicalized_mol_block'] is None for entry in data):
        print(f"Skipping session {npe.session} because canonicalized_mol_block is missing in one or more entries")
        continue

    # Add metadata fields
    for curator_entry in data:
        if npe.email in email_replacements:
            curator_entry['curator_email_address'] = email_replacements[npe.email]
        else:
            curator_entry['curator_email_address'] = npe.email
        curator_entry['session_uuid'] = npe.session
        curator_entry['rdkit_version'] = rdkit_version
        curator_entry['created_date'] = npe.created_date.isoformat()

    # Save JSON locally
    json_filename = f"npmrd_curator_{npe.session}.json"
    local_path = os.path.join(EXPORT_JSON_DIR, json_filename)
    with open(local_path, "w") as f:
        json.dump(data, f, indent=2)

    # Upload to S3
    try:
        s3.upload_file(local_path, ARCHIVE_S3_BUCKET_NAME, json_filename)
        print(f"Uploaded {json_filename} to S3 bucket {ARCHIVE_S3_BUCKET_NAME}")
    except Exception:
        print(f"Failed to upload {json_filename} to S3: {traceback.format_exc()}")

    # Send data to NP-MRD endpoint
    try:
        resp = requests.post(
            ENDPOINT_URL,
            headers={
                "Authorization": f"Bearer {NP_DEPOSITION_API_BEARER_TOKEN}",
                "Content-Type": "application/json",
                "accept": "*/*",
            },
            data=json.dumps(data)
        )
        resp.raise_for_status()
        # Mark as handled if successful
        npe.handled = True
        sess.add(npe)
        num_pushed += 1
        if num_pushed % print_threshold == 0:
            print(f"Pushed {num_pushed}/{len(new_npmrd_entries)} entries ({num_pushed / len(new_npmrd_entries) * 100:.0f}%)")
    except Exception as e:
        print(f"Failed to push entry session {npe.session} to NP-MRD: {e}")

# Commit handled flags
sess.commit()
sess.close()
print(f"Finished pushing {num_pushed} entries!")
