#%%
import os
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session


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
print(f"Got {len(new_npmrd_entries)}")
# %%
# write these entries to files
print("Writing entries to `./submissions` directory")
os.makedirs("./submissions", exist_ok=True)
for npe in new_npmrd_entries:
    data = json.loads(npe.data)
    with open(f"./submissions/npmrd_curator_{npe.session}.json", "w") as f:
        f.write(json.dumps(data, indent=2))


# %%
# WARNING - MAKE SURE YOU'RE ACTUALLY SENDING THESE TO THE NP-MRD DATABASE
# Mark these now saved entries and handles
resp1 = input("Do you want to mark these entries as handles? (y/N)").lower()
if resp1 == "y":
    print("New entries have been marked as handled")
    for npe in new_npmrd_entries:
        npe.handled = True
    sess.commit()
    sess.close()
else:
    print("Alright, the entries have been left alone in the DB")
