
from fastapi import APIRouter, Body
from rpg_project.src.services.reputation_singleton import reputation_manager


router = APIRouter()

@router.get("/character/reputation")
def get_reputation(character_id: str):
    """Gibt den aktuellen Ruf für alle Fraktionen des Charakters zurück."""
    return reputation_manager.get_api_state(character_id)

# Test-Endpunkt: Event an ReputationManager schicken (nur für Tests!)
@router.post("/test/event")
def test_event(event_type: str = Body(...), data: dict = Body(...)):
    """Löst ein Event im ReputationManager aus (nur für Integrationstests)."""
    reputation_manager.handle_event(event_type, data)
    return {"status": "ok"}
