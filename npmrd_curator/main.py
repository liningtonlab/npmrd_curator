import io
import json
from copy import deepcopy
from typing import Optional

import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware

import npmrd_curator.parsers.textblock_writer as tw
from npmrd_curator import chem
from npmrd_curator.database import Base, SessionLocal, Submission, engine
from npmrd_curator.schemas import (
    CatchAll,
    Format,
    Input,
    TableConvert,
    Submission as SubmissionData,
)

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/api/")
def status():
    return {"status": "good"}


@app.post("/api/parse_textblock")
def parse_textblock(data: Input):
    """Given text, try to parse into structured output"""
    with open("npmrd_curator/mock_jsonoutput.json") as f:
        d = json.load(f)
    return d


@app.post("/api/write_textblock")
def write_textblock(data: CatchAll):
    """Given structured output, reconstruct textblock"""
    return tw.write_all(data.dict().get("data"))


@app.post("/api/parse_table")
def parse_textblock(data: Input):
    """Given text, try to parse into csv table output"""
    df = pd.read_csv("npmrd_curator/mock_htmloutput.csv")

    return {
        "columns": list(df.columns),
        "data": df.replace({np.nan: "-"}).astype(str).to_dict(orient="records"),
        # Modified for frontend dev
        "num_compounds": 3,
    }


@app.post("/api/convert_table")
def convert_table(data: TableConvert):
    """Given curated table, convert it to structured JSON format"""
    with open("npmrd_curator/mock_jsonoutput.json") as f:
        d = json.load(f)
    return [deepcopy(d), deepcopy(d), deepcopy(d)]


@app.get(
    "/api/utils/structure/{inp}",
    responses={
        200: {
            "content": {
                "application/json": {},
                "chemical/x-mdl-sdfile": {},
                "image/svg+xml": {},
            },
            "description": "Return the text or sdf file.",
        }
    },
)
def convert_structure(inp: str, fmt: Format = Format.sdf, get3d: bool = False):
    try:
        out = chem.convert(structure=inp, fmt=fmt, get3d=get3d)
    except:
        raise HTTPException(400, detail="Structure could not be converted")
    if fmt == Format.sdf:
        return StreamingResponse(
            io.BytesIO(out.encode()), media_type="chemical/x-mdl-sdfile"
        )
    if fmt == Format.svg:
        return StreamingResponse(io.BytesIO(out.encode()), media_type="image/svg+xml")
    return


@app.post("/api/submit")
def submit_data(data: SubmissionData, db: Session = Depends(get_db)):
    db_data = Submission(
        session=data.session, doi=data.doi, email=data.email, data=json.dumps(data.data)
    )
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return {"status": "success", "session": data.session, "db_id": db_data.id}
