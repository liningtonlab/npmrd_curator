from typing import Dict, List

from pydantic import BaseModel, Extra
from enum import Enum


class Format(str, Enum):
    sdf = "sdf"
    inchi = "inchi"
    smiles = "smiles"


class CatchAll(BaseModel):
    class Config:
        extra = Extra.allow


class Input(BaseModel):
    data: str
