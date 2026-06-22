import math

class ItemManager:
    def __init__(self, magnet_range=64.0):
        self.dropped_items = []
        self.magnet_range = magnet_range

    def spawn_item(self, x, y, item_name, cooldown=5.0):
        self.dropped_items.append({
            "x": x,
            "y": y,
            "item": item_name,
            "cooldown": cooldown
        })

    def update(self, delta_time, player_x, player_y, player_add_item_callback):
        # Update Cooldown Drop Item
        for item in self.dropped_items:
            if item["cooldown"] > 0:
                item["cooldown"] -= delta_time

        # Deteksi Magnet Auto-pickup untuk item drop yang cooldownnya sudah habis
        for item in self.dropped_items[:]:
            if item["cooldown"] <= 0:
                dist = math.dist((player_x, player_y), (item["x"], item["y"]))
                if dist < self.magnet_range:
                    # Tarik item ke pemain
                    dx = player_x - item["x"]
                    dy = player_y - item["y"]
                    item["x"] += dx * 0.1
                    item["y"] += dy * 0.1

                    # Jika sangat dekat, masukkan ke inventory
                    if dist < 10:
                        if player_add_item_callback(item["item"]):
                            self.dropped_items.remove(item)
                        else:
                            # Jika penuh, dorong kembali sedikit agar tidak tersangkut loop pickup
                            item["cooldown"] = 1.0
