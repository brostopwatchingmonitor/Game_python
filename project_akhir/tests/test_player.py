import pytest
from core.player import Player

def test_player_initial_state():
    player = Player(x=150, y=200, speed=5.0)
    assert player.x == 150
    assert player.y == 200
    assert player.speed == 5.0
    assert player.inventory == ["Ramuan HP", "Elixir", "Kosong"]
    assert player.selected_slot == 0

def test_select_slot():
    player = Player()
    assert player.select_slot(1) is True
    assert player.selected_slot == 1
    assert player.select_slot(3) is False  # Invalid slot index
    assert player.selected_slot == 1  # Unchanged

def test_drop_item():
    player = Player()
    player.inventory = ["Ramuan HP", "Kosong", "Elixir"]
    
    # Drop from empty slot
    player.select_slot(1)
    assert player.drop_item() is None
    assert player.inventory[1] == "Kosong"

    # Drop from filled slot
    player.select_slot(0)
    assert player.drop_item() == "Ramuan HP"
    assert player.inventory[0] == "Kosong"

def test_add_item():
    player = Player()
    player.inventory = ["Kosong", "Kosong", "Kosong"]
    
    assert player.add_item("Gold Key") is True
    assert player.inventory == ["Gold Key", "Kosong", "Kosong"]
    
    assert player.add_item("Red Potion") is True
    assert player.inventory == ["Gold Key", "Red Potion", "Kosong"]
    
    assert player.add_item("Shield") is True
    assert player.inventory == ["Gold Key", "Red Potion", "Shield"]
    
    # Inventory is now full
    assert player.add_item("Sword") is False
    assert player.inventory == ["Gold Key", "Red Potion", "Shield"]

def test_update_position():
    player = Player(x=10, y=20)
    player.update_position(5, -15)
    assert player.x == 15
    assert player.y == 5
