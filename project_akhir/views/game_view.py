import arcade
import json
import math
from core.balancing import Balancing
from core.player import Player
from core.item_manager import ItemManager

class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.tile_map = None
        self.scene = None
        self.player_sprite = None
        self.physics_engine = None
        
        # Kamera
        self.camera = None
        self.gui_camera = None

        # Dialog Easter Egg
        self.sewage_position = None
        self.dialogue_active = False
        self.dialogue_text = ""
        self.dialogue_timer = 0.0

        # Kontrol input
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        # Load Balancing
        self.balancing_mgr = Balancing()
        self.balancing = self.balancing_mgr.data

        # Player Model
        self.player_model = Player(
            speed=self.balancing_mgr.get_player_setting("base_speed", 4.0)
        )

        # Item Manager Model
        self.item_manager = ItemManager(
            magnet_range=self.balancing_mgr.get_player_setting("magnet_range", 64.0)
        )

    # Properties untuk backward-compatibility dengan views lain / game loop asal
    @property
    def inventory(self):
        return self.player_model.inventory

    @inventory.setter
    def inventory(self, val):
        self.player_model.inventory = val

    @property
    def selected_slot(self):
        return self.player_model.selected_slot

    @selected_slot.setter
    def selected_slot(self, val):
        self.player_model.selected_slot = val

    @property
    def dropped_items(self):
        return self.item_manager.dropped_items

    @dropped_items.setter
    def dropped_items(self, val):
        self.item_manager.dropped_items = val

    def load_balancing_data(self):
        # Stub untuk compatibility
        self.balancing_mgr = Balancing()
        self.balancing = self.balancing_mgr.data

    def setup(self):
        # Set up Kamera
        self.camera = arcade.Camera2D()

        # Inisialisasi teks petunjuk HUD sekali saja
        self.hud_text = arcade.Text(
            "W/A/S/D: Gerak | Angka 1-3: Pilih Slot | Q: Drop Item | J: Interaksi Saluran Pembuangan", 
            10, self.window.height - 20, 
            arcade.color.LIGHT_YELLOW, 
            font_size=10
        )

        # Inisialisasi reusable text objects untuk optimasi performa
        self.item_label_text = arcade.Text("", 0, 0, arcade.color.WHITE, font_size=8, anchor_x="center")
        self.inventory_slot_text = arcade.Text("", 0, 0, arcade.color.WHITE, font_size=10)
        self.dialogue_bubble_text = arcade.Text("", 0, 0, arcade.color.BLACK, font_size=8, anchor_x="center", width=380, align="center")

        # Load Tiled Map
        map_name = "assets/maps/dungeon_level1.tmx"
        
        # Konfigurasi layer khusus untuk tembok tabrakan
        layer_options = {
            "Walls": {
                "use_spatial_hash": True,
            }
        }
        
        self.tile_map = arcade.tilemap.load_tilemap(map_name, scaling=2.0, layer_options=layer_options)
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # Cari posisi spawn
        spawn_list = self.tile_map.object_lists.get("Objects", [])
        player_x = 100
        player_y = 100
        print(f"[DEBUG] Jumlah objek di map: {len(spawn_list)}")
        for obj in spawn_list:
            # Mengambil koordinat X dan Y secara aman bergantung tipe shape
            if isinstance(obj.shape, list):
                ox = obj.shape[0][0]
                oy = obj.shape[0][1]
            else:
                ox = obj.shape[0]
                oy = obj.shape[1]
            print(f"[DEBUG] Objek ditemukan: {obj.name} di koordinat ({ox}, {oy})")

            if obj.name == "PlayerSpawn":
                player_x = ox
                player_y = oy
            elif obj.name == "SewageDrain":
                self.sewage_position = (ox, oy)

        # Buat Player Sprite (Menggunakan visualisasi sprite solid yang lebih jelas terlihat, 16x16 piksel)
        self.player_sprite = arcade.SpriteSolidColor(16, 16, arcade.color.DARK_RED)
        self.player_sprite.center_x = player_x
        self.player_sprite.center_y = player_y
        
        # Sync coordinates ke Player Model
        self.player_model.x = player_x
        self.player_model.y = player_y

        print(f"[DEBUG] Player berhasil dibuat di posisi: ({player_x}, ({player_y})")
        self.scene.add_sprite("Player", self.player_sprite)

        # Buat sprite list untuk item drop
        self.scene.add_sprite_list("Drops")

        # Buat Physics Engine (hanya menyertakan layer Walls)
        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite,
            walls=self.scene["Walls"]
        )
    def on_draw(self):
        self.clear()

        # Gunakan kamera gameplay
        self.camera.use()
        self.scene.draw(pixelated=True)

        # Gambar item drop di tanah
        for item in self.dropped_items:
            arcade.draw_rect_filled(
                arcade.rect.XYWH(item["x"], item["y"], 8, 8),
                arcade.color.GOLD
            )
            # Update reusable text properties lalu render
            self.item_label_text.text = item["item"]
            self.item_label_text.x = item["x"]
            self.item_label_text.y = item["y"] + 8
            self.item_label_text.draw()


        # Aktifkan kamera GUI untuk teks UI statis
        self.window.default_camera.use()

        # Tampilkan Quick Inventory HUD
        for i in range(3):
            color = arcade.color.GOLDENROD if i == self.selected_slot else arcade.color.GRAY
            border = 3 if i == self.selected_slot else 1
            x_pos = 50 + (i * 120)
            arcade.draw_rect_outline(
                arcade.rect.XYWH(x_pos + 50, 50, 100, 40),
                color,
                border_width=border
            )
            # Update reusable text properties lalu render
            self.inventory_slot_text.text = f"{i+1}: {self.inventory[i]}"
            self.inventory_slot_text.x = x_pos + 10
            self.inventory_slot_text.y = 42
            self.inventory_slot_text.draw()

        # Gambar dialog gelembung komik jika aktif
        if self.dialogue_active:
            cam_x, cam_y = self.camera.position
            screen_x = self.player_sprite.center_x - (cam_x - self.window.width / 2)
            screen_y = self.player_sprite.center_y - (cam_y - self.window.height / 2) + 40
            
            # Gambar background dialog komik
            arcade.draw_rect_filled(
                arcade.rect.XYWH(screen_x, screen_y, 400, 50),
                arcade.color.WHITE
            )
            arcade.draw_rect_outline(
                arcade.rect.XYWH(screen_x, screen_y, 400, 50),
                arcade.color.BLACK,
                border_width=2
            )
            # Update reusable text properties lalu render
            self.dialogue_bubble_text.text = self.dialogue_text
            self.dialogue_bubble_text.x = screen_x
            self.dialogue_bubble_text.y = screen_y - 6
            self.dialogue_bubble_text.draw()

        # Petunjuk HUD
        if hasattr(self, "hud_text") and self.hud_text:
            self.hud_text.draw()

    def center_camera_to_player(self):
        # Di Arcade 3.x, self.camera.position adalah PUSAT (center) kamera.
        # Jadi kita cukup mengarahkan posisi kamera langsung ke pusat player sprite.
        self.camera.position = (self.player_sprite.center_x, self.player_sprite.center_y)

    def on_update(self, delta_time):
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        speed = self.player_model.speed

        if self.up_pressed and not self.down_pressed:
            self.player_sprite.change_y = speed
        elif self.down_pressed and not self.up_pressed:
            self.player_sprite.change_y = -speed
        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -speed
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = speed

        self.physics_engine.update()
        
        # Sync coordinates ke Player Model
        self.player_model.x = self.player_sprite.center_x
        self.player_model.y = self.player_sprite.center_y

        self.center_camera_to_player()

        # Update Item Manager (cooldowns & magnet system)
        self.item_manager.update(
            delta_time,
            self.player_model.x,
            self.player_model.y,
            self.player_model.add_item
        )

        # Update durasi timer dialog komik
        if self.dialogue_active:
            self.dialogue_timer -= delta_time
            if self.dialogue_timer <= 0:
                self.dialogue_active = False

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W or key == arcade.key.UP:
            self.up_pressed = True
        elif key == arcade.key.S or key == arcade.key.DOWN:
            self.down_pressed = True
        elif key == arcade.key.A or key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.D or key == arcade.key.RIGHT:
            self.right_pressed = True
            
        # Pilihan Slot Inventory
        elif key == arcade.key.KEY_1:
            self.player_model.select_slot(0)
        elif key == arcade.key.KEY_2:
            self.player_model.select_slot(1)
        elif key == arcade.key.KEY_3:
            self.player_model.select_slot(2)

        # Drop item yang dipilih (Q)
        elif key == arcade.key.Q:
            dropped_item = self.player_model.drop_item()
            if dropped_item:
                self.item_manager.spawn_item(
                    self.player_model.x,
                    self.player_model.y - 20,
                    dropped_item,
                    cooldown=5.0
                )

        # Interaksi J (Easter Egg Saluran Pembuangan)
        elif key == arcade.key.J:
            if self.sewage_position:
                dist = math.dist(
                    (self.player_sprite.center_x, self.player_sprite.center_y),
                    self.sewage_position
                )
                if dist < 48:
                    self.dialogue_active = True
                    self.dialogue_text = "Seseorang pernah masuk ke sini, tapi anehnya sekarang dia jadi orang penting di pemerintahan."
                    self.dialogue_timer = 5.0

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W or key == arcade.key.UP:
            self.up_pressed = False
        elif key == arcade.key.S or key == arcade.key.DOWN:
            self.down_pressed = False
        elif key == arcade.key.A or key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.D or key == arcade.key.RIGHT:
            self.right_pressed = False
