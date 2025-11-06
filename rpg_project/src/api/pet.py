from fastapi import APIRouter, Body
from pydantic import BaseModel
from rpg_project.src.models.pet import Pet
from rpg_project.src.services.pet_ai import PetAI
import json5

router = APIRouter()

# Dummy-Loader für Pets (aus Config)
def load_pets():
    with open("config/pets.json5", "r") as f:
        data = json5.load(f)
        return [Pet(**pet) for pet in data]

ALL_PETS = {pet.id: pet for pet in load_pets()}

class SummonRequest(BaseModel):
    pet_id: str

@router.post("/pet/summon")
def summon_pet(request: SummonRequest = Body(...)):
    pet = ALL_PETS.get(request.pet_id)
    if not pet:
        return {"error": "Pet nicht gefunden"}
    # In echt: Pet zum Spieler hinzufügen
    return {"pet": pet.dict()}

class CommandRequest(BaseModel):
    pet_id: str
    battle_context: dict

@router.post("/pet/command")
def command_pet(request: CommandRequest = Body(...)):
    pet = ALL_PETS.get(request.pet_id)
    if not pet:
        return {"error": "Pet nicht gefunden"}
    ai = PetAI(pet)
    action = ai.decide_action(request.battle_context)
    return {"action": action}
