class Player:
    def __init__(self, x=100.0, y=100.0, speed=4.0):
        self.x = x
        self.y = y
        self.speed = speed
        self.inventory = ["Ramuan HP", "Elixir", "Kosong"]
        self.selected_slot = 0  # 0-indexed (tombol 1, 2, 3)

    def select_slot(self, slot_idx):
        if 0 <= slot_idx <= 2:
            self.selected_slot = slot_idx
            return True
        return False

    def drop_item(self):
        item_name = self.inventory[self.selected_slot]
        if item_name != "Kosong":
            self.inventory[self.selected_slot] = "Kosong"
            return item_name
        return None

    def add_item(self, item_name):
        for idx in range(3):
            if self.inventory[idx] == "Kosong":
                self.inventory[idx] = item_name
                return True
        return False

    def update_position(self, dx, dy):
        self.x += dx
        self.y += dy
