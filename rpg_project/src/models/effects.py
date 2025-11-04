
from pydantic import BaseModel


class Effect(BaseModel):
    """Repräsentiert einen Status-Effekt (z.B. Brennen, Gift, Buffs).
    """

    name: str  # z.B. "Brennen"
    duration: int  # Rundenanzahl
    damage_per_tick: int | None = 0  # Schaden pro Tick (z.B. Brennen)
    # Weitere Felder: stat_modifiers, stacking, etc. möglich
