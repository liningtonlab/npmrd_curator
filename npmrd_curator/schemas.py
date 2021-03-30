from typing import Dict, List, Optional

from pydantic import BaseModel, Extra
from enum import Enum


class TableFormat(str, Enum):
    html = "html"
    tsv = "tsv"


class Format(str, Enum):
    sdf = "sdf"
    inchi = "inchi"
    smiles = "smiles"
    svg = "svg"


class CatchAll(BaseModel):
    class Config:
        extra = Extra.allow


class Input(BaseModel):
    data: str


class TableConvert(BaseModel):
    columns: List[str]
    data: List[Dict]
    names: List[str]
    smiles: List[str]


class Submission(BaseModel):
    session: str
    doi: Optional[str] = None
    email: Optional[str] = None
    data: List[Dict]
