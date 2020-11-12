from typing import Dict, List

from pydantic import BaseModel, Extra


class CatchAll(BaseModel):
    class Config:
        extra = Extra.allow


class Input(BaseModel):
    data: str
