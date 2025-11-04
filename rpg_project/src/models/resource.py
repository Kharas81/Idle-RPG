from pydantic import BaseModel

class Resource(BaseModel):
    """
    Repräsentiert eine sammelbare Ressource (z.B. Eisenerz, Holz).
    """
    name: str
    type: str  # z.B. "mineral", "wood", "herb"
    amount: int = 1
