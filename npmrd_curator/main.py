import io
import json
from typing import Optional

import pandas as pd
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from starlette.middleware.cors import CORSMiddleware

import npmrd_curator.parsers.textblock_writer as tw
from npmrd_curator import chem
from npmrd_curator.schemas import CatchAll, Format, Input

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/")
def read_root():
    return {"status": "good"}


@app.post("/api/parse_textblock")
def parse_textblock(data: Input):
    """Given text, try to parse into structured output"""
    with open(
        "/home/jvansan/git/npmrd_curator/npmrd_curator/mock_jsonoutput.json"
    ) as f:
        d = json.load(f)
    return d


@app.post("/api/write_textblock")
def write_textblock(data: CatchAll):
    """Given structured output, reconstruct textblock"""
    return tw.write_all(data.dict().get("data"))


@app.post("/api/parse_table")
def parse_textblock(data: Input):
    """Given text, try to parse into csv table output"""
    df = pd.read_csv(
        "/home/jvansan/git/npmrd_curator/npmrd_curator/mock_htmloutput.csv"
    )

    return {
        "columns": list(df.columns),
        "data": df.replace({pd.np.nan: "-"}).astype(str).to_dict(orient="records"),
    }


@app.get(
    "/api/utils/structure/{inp}",
    responses={
        200: {
            "content": {"application/json": {}, "chemical/x-mdl-sdfile": {},},
            "description": "Return the text or sdf file.",
        }
    },
)
def convert_structure(inp: str, fmt: Format = Format.sdf, get3d: bool = False):
    out = chem.convert(structure=inp, fmt=fmt, get3d=get3d)
    if fmt == Format.sdf:
        return StreamingResponse(
            io.BytesIO(out.encode()), media_type="chemical/x-mdl-sdfile"
        )
    return
