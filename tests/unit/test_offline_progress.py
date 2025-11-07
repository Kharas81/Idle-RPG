import time
from rpg_project.src.services.offline_progress import OfflineProgressCalculator

def test_offline_progress_calculation():
    calc = OfflineProgressCalculator()
    # Simuliere 60 Minuten Offline-Zeit
    last_logout = 1000000.0
    now = last_logout + 60 * 60  # 1 Stunde später
    result = calc.calculate(last_logout, now)
    assert result["minutes"] == 60
    assert result["xp"] == 120  # 60 * 2 xp_per_minute laut Config
    assert result["gold"] == 60
    assert result["resources"] == 0

    # Teste Begrenzung auf max_offline_minutes (z.B. 800 Minuten -> 720)
    now = last_logout + 800 * 60
    result = calc.calculate(last_logout, now)
    assert result["minutes"] == 720
    assert result["xp"] == 1440
    assert result["gold"] == 720
    assert result["resources"] == 0
