import os
import tempfile
import json
import pytest
from core.balancing import Balancing

def test_default_balancing_fallback():
    # Test fallback data when file does not exist
    balancing = Balancing(filepath="non_existent_file.json")
    assert "player" in balancing.data
    assert balancing.get_player_setting("base_speed") == 4.0
    assert balancing.get_player_setting("magnet_range") == 64.0

def test_load_balancing_from_file():
    # Test reading data from actual JSON file format
    mock_data = {
        "player": {
            "base_speed": 5.5,
            "magnet_range": 80.0,
            "base_hp": 120
        },
        "enemies": {
            "slime": {
                "hp": 25,
                "speed": 2.0
            }
        },
        "items": {
            "health_potion": {
                "heal_amount": 50
            }
        }
    }
    
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(mock_data, f)
        temp_path = f.name
        
    try:
        balancing = Balancing(filepath=temp_path)
        assert balancing.get_player_setting("base_speed") == 5.5
        assert balancing.get_player_setting("magnet_range") == 80.0
        assert balancing.get_enemy_setting("slime", "hp") == 25
        assert balancing.get_item_setting("health_potion", "heal_amount") == 50
    finally:
        os.remove(temp_path)
