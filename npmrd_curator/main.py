import io
from typing import Optional
import json

import pandas as pd
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from starlette.middleware.cors import CORSMiddleware

from npmrd_curator.schemas import CatchAll, Input
import npmrd_curator.parsers.textblock_writer as tw

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
