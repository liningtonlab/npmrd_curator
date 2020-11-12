from typing import Optional

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from npmrd_curator.schemas import CatchAll

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


@app.get("/api/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.post("/api/parse_textblock")
def parse_textblock(data: Input):
    """Given text, try to parse into structured output"""
    return f"Fake textblock, {data.dict()}"


@app.post("/api/write_textblock")
def write_textblock(data: CatchAll):
    """Given structured output, reconstruct textblock"""
    return f"Fake textblock, {data.dict()}"


@app.post("/api/parse_table")
def parse_textblock(data: Input):
    """Given text, try to parse into csv table output"""
    return f"Fake textblock, {data.dict()}"
