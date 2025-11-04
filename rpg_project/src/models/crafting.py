from pydantic import BaseModel
from typing import List

class CraftingInput(BaseModel):
    name: str
    amount: int

class CraftingOutput(BaseModel):
    name: str
    amount: int

class Recipe(BaseModel):
    name: str
    inputs: List[CraftingInput]
    outputs: List[CraftingOutput]
