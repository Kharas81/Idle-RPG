"""
API-Endpunkte für Ausrüstung: /character/equip und /character/unequip
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from rpg_project.src.services.equipment_service import EquipmentService
from rpg_project.src.services.config_loader import ConfigLoader
from rpg_project.src.models.character import Character

router = APIRouter()

# Dummy: Session/Charakterverwaltung muss im echten System angebunden werden
active_character = Character(name="Held", stats={"ATK": 1}, equipment={})
items_config = {item["id"]: item for item in ConfigLoader.load_config("config/items.json5")}
equipment_service = EquipmentService(items_config)

class EquipRequest(BaseModel):
    item_id: str

class UnequipRequest(BaseModel):
    slot: str

@router.post("/character/equip")
def equip_item(req: EquipRequest):
    success = equipment_service.equip(active_character, req.item_id)
    if not success:
        raise HTTPException(status_code=400, detail="Item konnte nicht angelegt werden.")
    return {"success": True, "equipment": active_character.equipment, "stats": active_character.stats}

@router.post("/character/unequip")
def unequip_item(req: UnequipRequest):
    success = equipment_service.unequip(active_character, req.slot)
    if not success:
        raise HTTPException(status_code=400, detail="Slot war leer oder ungültig.")
    return {"success": True, "equipment": active_character.equipment, "stats": active_character.stats}
