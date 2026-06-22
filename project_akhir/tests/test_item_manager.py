import pytest
from core.item_manager import ItemManager

def test_spawn_item():
    manager = ItemManager()
    manager.spawn_item(10.0, 20.0, "Iron Ore", cooldown=3.0)
    assert len(manager.dropped_items) == 1
    assert manager.dropped_items[0]["item"] == "Iron Ore"
    assert manager.dropped_items[0]["cooldown"] == 3.0

def test_update_cooldown():
    manager = ItemManager()
    manager.spawn_item(10.0, 20.0, "Iron Ore", cooldown=3.0)
    
    # Callback returns False (should not pick up during cooldown)
    def dummy_callback(item):
        return True

    manager.update(1.0, 10.0, 20.0, dummy_callback)
    assert manager.dropped_items[0]["cooldown"] == 2.0

def test_magnet_pull_and_pickup():
    manager = ItemManager(magnet_range=50.0)
    # Spawn item at distance 30, with cooldown 0 (ready to be pulled/picked up)
    manager.spawn_item(40.0, 0.0, "Coin", cooldown=0.0)
    
    # Player at (0, 0)
    inventory = []
    def add_to_inventory(item):
        inventory.append(item)
        return True

    # First update: distance is 40 < magnet_range, item should pull closer to player
    manager.update(0.1, 0.0, 0.0, add_to_inventory)
    assert len(manager.dropped_items) == 1
    item = manager.dropped_items[0]
    # Check that x has decreased towards 0 (was 40, now pulls towards 0)
    assert item["x"] < 40.0
    
    # Teleport player to exactly on top of the item to trigger immediate pickup
    manager.update(0.1, item["x"], item["y"], add_to_inventory)
    assert len(manager.dropped_items) == 0
    assert inventory == ["Coin"]

def test_pickup_inventory_full():
    manager = ItemManager(magnet_range=50.0)
    manager.spawn_item(0.0, 0.0, "Coin", cooldown=0.0)
    
    # Inventory is full, so callback returns False
    def add_failed(item):
        return False
        
    manager.update(0.1, 0.0, 0.0, add_failed)
    # Item should still be on the ground, but its cooldown reset to 1.0
    assert len(manager.dropped_items) == 1
    assert manager.dropped_items[0]["cooldown"] == 1.0
