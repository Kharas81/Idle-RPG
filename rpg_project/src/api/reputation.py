from fastapi import APIRouter, Depends
from rpg_project.src.services.reputation_manager import ReputationManager
from rpg_project.src.api.game_state import get_current_character_id

router = APIRouter()
reputation_manager = ReputationManager()

@router.get("/character/reputation")
def get_reputation(character_id: str = Depends(get_current_character_id)):
    """Gibt den aktuellen Ruf für alle Fraktionen des Charakters zurück."""
    return reputation_manager.get_api_state(character_id)
