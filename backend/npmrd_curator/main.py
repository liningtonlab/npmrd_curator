import io
import json
import traceback
from copy import deepcopy
from typing import Optional

import numpy as np
import pandas as pd
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware

import npmrd_curator.parsers.html_table_parser as htmlp
import npmrd_curator.parsers.textblock_parser as textp
import npmrd_curator.parsers.textblock_writer as textw
import npmrd_curator.parsers.tsv_parser as tsvp
from npmrd_curator import chem
from npmrd_curator.database import Base, SessionLocal, Submission, engine
from npmrd_curator.schemas import CatchAll, Format, Input
from npmrd_curator.schemas import Submission as SubmissionData
from npmrd_curator.schemas import TableConvert, TableFormat

Base.metadata.create_all(bind=engine)

app = FastAPI(openapi_url="/api/openapi.json", docs_url="/api/docs")

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
    return textp.parse_text(data.data)


@app.post("/api/write_textblock")
def write_textblock(data: CatchAll):
    """Given structured output, reconstruct textblock"""
    return textw.write_all(data.dict().get("data"))  # type: ignore


@app.post("/api/parse_table")
def parse_table(data: Input, fmt: TableFormat = TableFormat.html):
    """Given text, try to parse into df table output"""
    try:
        if fmt == TableFormat.html:
            df, n_comp = htmlp.parse_html_str(data.data)
        elif fmt == TableFormat.tsv:
            df, n_comp = tsvp.parse_tsv_str(data.data)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(500, detail=str(e))
    return {
        "columns": list(df.columns),
        "data": df.replace({np.nan: "-"}).astype(str).to_dict(orient="records"),
        "num_compounds": n_comp,
    }


@app.post("/api/convert_table")
def convert_table(data: TableConvert):
    """Given curated table, convert it to structured JSON format"""
    try:
        output = htmlp.convert_grid_to_json(data.data, len(data.names))
        for i, n in enumerate(data.names):
            output[i]["smiles"] = data.smiles[i]
            output[i]["name"] = n
    except Exception as e:
        raise HTTPException(500, detail=str(e))
    return output


@app.get(
    "/api/utils/structure/{inp:path}",
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


@app.get("/api/summary")
def data_summary(db: Session = Depends(get_db)):
    """Get a summary of data in DB included total and previously unhandled"""
    total_data = db.query(Submission).count()
    unhandled_data = db.query(Submission).filter(Submission.handled == False).count()
    return {"total_data": total_data, "unhandled_data": unhandled_data}