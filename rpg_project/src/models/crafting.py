
from pydantic import BaseModel


class CraftingInput(BaseModel):
    name: str
    amount: int

class CraftingOutput(BaseModel):
    name: str
    amount: int

class Recipe(BaseModel):
    name: str
    inputs: list[CraftingInput]
    outputs: list[CraftingOutput]
