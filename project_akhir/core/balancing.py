import json
import os

class Balancing:
    def __init__(self, filepath=None):
        if filepath is None:
            # Menggunakan path absolut / relatif yang kokoh
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.filepath = os.path.join(base_dir, "database", "balancing.json")
        else:
            self.filepath = filepath
        self.data = self.load_data()

    def load_data(self):
        try:
            with open(self.filepath, "r") as f:
                return json.load(f)
        except Exception:
            # Fallback data jika file tidak terbaca
            return {
                "player": {
                    "base_speed": 4.0,
                    "magnet_range": 64.0,
                    "base_hp": 100
                },
                "items": {},
                "enemies": {}
            }

    def get_player_setting(self, key, default=None):
        return self.data.get("player", {}).get(key, default)

    def get_enemy_setting(self, enemy_type, key, default=None):
        return self.data.get("enemies", {}).get(enemy_type, {}).get(key, default)

    def get_item_setting(self, item_type, key, default=None):
        return self.data.get("items", {}).get(item_type, {}).get(key, default)
