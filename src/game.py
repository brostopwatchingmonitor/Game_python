# game.py
import pygame
import sys
import os
import random
import json
from pytmx.util_pygame import load_pygame
from settings import *
from player import Player
from sprites import Tile
from groups import CameraGroup
from enemy import BaseEnemy
from dialogue import DialogueManager

class Game:
    def __init__(self):
        pygame.init()
        # Window utama (screen fisik)
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("2D Platformer - Void Mermaid Action")
        
        # Canvas internal untuk rendering pixel art
        self.display_surface = pygame.Surface((RENDER_WIDTH, RENDER_HEIGHT))
        
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Sprite Groups
        self.all_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group()
        self.background_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        
        # Sistem Respawn Musuh
        self.respawn_queue = []
        
        # Load Map dan Spawn Entitas
        self.setup_map()

        # Inisialisasi Sistem Dialog Visual Novel (Awal Game)
        self.dialogue_manager = DialogueManager()
        self.state = "dialogue"
        self.dialogue_manager.start_cutscene("intro_stage_0", self.end_dialogue)

    def setup_map(self):
        self.all_sprites.empty()
        self.collision_sprites.empty()
        self.background_sprites.empty()
        self.enemy_sprites.empty()
        self.respawn_queue.clear()
        
        tmx_path = os.path.join(ASSETS_DIR, 'image', 'maps', 'forest.tmx')
        try:
            tmx_data = load_pygame(tmx_path)
        except Exception as e:
            print(f"[Game] Gagal memuat peta TMX dari {tmx_path}: {e}")
            tmx_data = None
            
        if tmx_data:
            tile_scale = 2
            scaled_tile_w = tmx_data.tilewidth * tile_scale
            scaled_tile_h = tmx_data.tileheight * tile_scale
            
            self.all_sprites.map_width = tmx_data.width * scaled_tile_w
            self.all_sprites.map_height = tmx_data.height * scaled_tile_h

            for layer in tmx_data.visible_layers:
                if hasattr(layer, 'data'):
                    for x, y, surf in layer.tiles():
                        pos = (x * scaled_tile_w, y * scaled_tile_h)
                        scaled_surf = pygame.transform.scale(surf, (scaled_tile_w, scaled_tile_h))
                        
                        if layer.name in ('ground', 'wood'):
                            groups = (self.all_sprites, self.collision_sprites)
                            Tile(pos, scaled_surf, groups)
                        else:
                            groups = (self.all_sprites, self.background_sprites)
                            Tile(pos, scaled_surf, groups)

            player_pos = (50, 100)
            for obj in tmx_data.objects:
                if obj.name == 'player':
                    player_pos = (obj.x * tile_scale, obj.y * tile_scale)
                    break
                    
            self.player = Player(player_pos, self.all_sprites, self.collision_sprites, self.enemy_sprites)

            for obj in tmx_data.objects:
                if obj.name == 'enemy':
                    enemy_pos = (obj.x * tile_scale, obj.y * tile_scale)
                    enemy_type = 'tier_1' if random.random() < 0.6 else 'tier_2'
                    BaseEnemy(enemy_pos, enemy_type, (self.all_sprites, self.enemy_sprites), self.collision_sprites, self.player, self)
        else:
            self.player = Player((100, 200), self.all_sprites, self.collision_sprites, self.enemy_sprites)
            BaseEnemy((300, 200), 'tier_1', (self.all_sprites, self.enemy_sprites), self.collision_sprites, self.player, self)

        self.load_save()

    def end_dialogue(self):
        # Callback saat dialog selesai/dilewati
        self.state = STATE_PLAYING
        print("[Dialogue] Dialog selesai atau dilewati. Memulai permainan!")

    def auto_save(self):
        save_data = {
            "level": self.player.level,
            "xp": self.player.xp,
            "xp_to_next_level": self.player.xp_to_next_level,
            "hp": self.player.max_hp, 
            "max_hp": self.player.max_hp,
            "score": self.player.score,
            "base_attack_damage": self.player.base_attack_damage,
            "speed": self.player.speed
        }
        try:
            with open("autosave.json", "w") as f:
                json.dump(save_data, f, indent=2)
            print("[AutoSave] Progres berhasil disimpan otomatis saat karakter mati.")
        except Exception as e:
            print(f"[AutoSave] Gagal menyimpan progres otomatis: {e}")

    def load_save(self):
        if os.path.exists("autosave.json"):
            try:
                with open("autosave.json", "r") as f:
                    data = json.load(f)
                self.player.level = data.get("level", 1)
                self.player.xp = data.get("xp", 0)
                self.player.xp_to_next_level = data.get("xp_to_next_level", 100)
                self.player.max_hp = data.get("max_hp", 100)
                self.player.hp = self.player.max_hp
                self.player.score = data.get("score", 0)
                self.player.base_attack_damage = data.get("base_attack_damage", 20)
                self.player.speed = data.get("speed", 200)
                print(f"[AutoSave] Progres dimuat. Level: {self.player.level}, DMG: {self.player.base_attack_damage}")
            except Exception as e:
                print(f"[AutoSave] Gagal memuat progres: {e}")

    def queue_respawn(self, pos, enemy_type):
        respawn_time = pygame.time.get_ticks() + 5000
        self.respawn_queue.append({
            'pos': pos,
            'type': enemy_type,
            'time': respawn_time
        })
        print(f"[Respawn] Musuh jenis {enemy_type} didaftarkan. Respawn dalam 5 detik.")

    def check_respawns(self):
        current_time = pygame.time.get_ticks()
        to_respawn = [item for item in self.respawn_queue if current_time >= item['time']]
        for item in to_respawn:
            BaseEnemy(item['pos'], item['type'], (self.all_sprites, self.enemy_sprites), self.collision_sprites, self.player, self)
            self.respawn_queue.remove(item)
            print(f"[Respawn] Musuh di {item['pos']} telah muncul kembali!")

    def draw_hud(self):
        hud_panel = pygame.Surface((180, 64), pygame.SRCALPHA)
        hud_panel.fill((20, 20, 30, 180))
        self.display_surface.blit(hud_panel, (8, 8))
        
        font_small = pygame.font.SysFont("Impact", 10)
        text_name = font_small.render(f"HASUMI (LV. {self.player.level})", True, (255, 255, 255))
        self.display_surface.blit(text_name, (14, 12))
        
        pygame.draw.rect(self.display_surface, (100, 20, 20), (14, 24, 120, 8))
        hp_ratio = self.player.hp / self.player.max_hp
        hp_color = (60, 220, 100) if hp_ratio > 0.4 else (255, 60, 60)
        pygame.draw.rect(self.display_surface, hp_color, (14, 24, int(120 * hp_ratio), 8))
        
        font_hp = pygame.font.SysFont("Arial", 8, bold=True)
        text_hp_val = font_hp.render(f"{self.player.hp}/{self.player.max_hp}", True, (255, 255, 255))
        self.display_surface.blit(text_hp_val, (138, 23))

        pygame.draw.rect(self.display_surface, (20, 40, 80), (14, 34, 120, 4))
        xp_ratio = min(1.0, self.player.xp / self.player.xp_to_next_level)
        pygame.draw.rect(self.display_surface, (50, 160, 255), (14, 34, int(120 * xp_ratio), 4))
        
        text_xp_val = font_hp.render(f"XP:{self.player.xp}/{self.player.xp_to_next_level}", True, (200, 220, 255))
        self.display_surface.blit(text_xp_val, (138, 32))

        font_score = pygame.font.SysFont("Impact", 11)
        text_score = font_score.render(f"COINS: {self.player.score}  [DMG: {self.player.base_attack_damage}]", True, (255, 210, 50))
        self.display_surface.blit(text_score, (14, 42))
        
        text_shop_hint = font_small.render("[TEKAN B: TOKO]", True, (150, 150, 200))
        self.display_surface.blit(text_shop_hint, (100, 12))
        
        if self.player.is_shielding:
            font_shield = pygame.font.SysFont("Impact", 10)
            text_shield = font_shield.render("SHIELD ACTIVE", True, (0, 220, 255))
            self.display_surface.blit(text_shield, (90, 42))

    def check_collisions(self):
        if self.player.hp <= 0:
            return
            
        hits = pygame.sprite.spritecollide(self.player, self.enemy_sprites, False)
        for enemy in hits:
            if not enemy.is_dead:
                knockback_dir = 1 if enemy.rect.centerx < self.player.rect.centerx else -1
                self.player.take_damage(enemy.damage, knockback_dir)

    def draw_game_over(self):
        overlay = pygame.Surface((RENDER_WIDTH, RENDER_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.display_surface.blit(overlay, (0, 0))
        
        font_title = pygame.font.SysFont("Impact", 36)
        text_title = font_title.render("GAME OVER", True, (255, 50, 50))
        rect_title = text_title.get_rect(center=(RENDER_WIDTH / 2, RENDER_HEIGHT / 2 - 20))
        self.display_surface.blit(text_title, rect_title)
        
        font_sub = pygame.font.SysFont("Arial", 12)
        text_sub = font_sub.render("Tekan 'R' untuk Restart Level atau 'M' untuk Keluar Game", True, (220, 220, 220))
        rect_sub = text_sub.get_rect(center=(RENDER_WIDTH / 2, RENDER_HEIGHT / 2 + 20))
        self.display_surface.blit(text_sub, rect_sub)

    def draw_shop(self):
        overlay = pygame.Surface((RENDER_WIDTH, RENDER_HEIGHT), pygame.SRCALPHA)
        overlay.fill((10, 10, 15, 220))
        self.display_surface.blit(overlay, (0, 0))
        
        shop_width = 400
        shop_height = 240
        shop_rect = pygame.Rect((RENDER_WIDTH - shop_width) / 2, (RENDER_HEIGHT - shop_height) / 2, shop_width, shop_height)
        pygame.draw.rect(self.display_surface, (25, 25, 35), shop_rect, border_radius=10)
        pygame.draw.rect(self.display_surface, (0, 220, 255), shop_rect, width=2, border_radius=10)
        
        font_title = pygame.font.SysFont("Impact", 20)
        text_title = font_title.render("TOKO SENJATA HASUMI", True, (0, 220, 255))
        rect_title = text_title.get_rect(center=(RENDER_WIDTH / 2, shop_rect.top + 25))
        self.display_surface.blit(text_title, rect_title)
        
        font_info = pygame.font.SysFont("Impact", 12)
        text_coins = font_info.render(f"KOIN ANDA: {self.player.score}", True, (255, 210, 50))
        self.display_surface.blit(text_coins, (shop_rect.left + 25, shop_rect.top + 50))
        
        font_item = pygame.font.SysFont("Arial", 11, bold=True)
        font_desc = pygame.font.SysFont("Arial", 10)
        
        item1_title = font_item.render("[1] PEDANG TAJAM (Base DMG +10) - Biaya: 300 Koin", True, (255, 255, 255))
        item1_desc = font_desc.render("Meningkatkan damage dasar tebasan pedang Anda.", True, (170, 170, 170))
        self.display_surface.blit(item1_title, (shop_rect.left + 25, shop_rect.top + 80))
        self.display_surface.blit(item1_desc, (45 + shop_rect.left, shop_rect.top + 95))
        
        item2_title = font_item.render("[2] RAMUAN DARAH (Pulihkan HP) - Biaya: 200 Koin", True, (255, 255, 255))
        item2_desc = font_desc.render("Memulihkan darah (HP) karakter kembali penuh 100%.", True, (170, 170, 170))
        self.display_surface.blit(item2_title, (shop_rect.left + 25, shop_rect.top + 120))
        self.display_surface.blit(item2_desc, (45 + shop_rect.left, shop_rect.top + 135))
        
        item3_title = font_item.render("[3] SEPATU KILAT (Speed +30%) - Biaya: 400 Koin", True, (255, 255, 255))
        item3_desc = font_desc.render("Meningkatkan kecepatan lari karakter secara permanen.", True, (170, 170, 170))
        self.display_surface.blit(item3_title, (shop_rect.left + 25, shop_rect.top + 160))
        self.display_surface.blit(item3_desc, (45 + shop_rect.left, shop_rect.top + 175))
        
        font_msg = pygame.font.SysFont("Arial", 10, italic=True)
        text_msg = font_msg.render(self.shop_message, True, self.shop_message_color)
        rect_msg = text_msg.get_rect(center=(RENDER_WIDTH / 2, shop_rect.bottom - 35))
        self.display_surface.blit(text_msg, rect_msg)
        
        font_hint = pygame.font.SysFont("Arial", 9)
        text_hint = font_hint.render("Tekan 'B' untuk menutup Toko dan kembali bermain.", True, (150, 150, 150))
        rect_hint = text_hint.get_rect(center=(RENDER_WIDTH / 2, shop_rect.bottom - 15))
        self.display_surface.blit(text_hint, rect_hint)

    def buy_item(self, item_num):
        if item_num == 1:
            cost = 300
            if self.player.score >= cost:
                self.player.score -= cost
                self.player.base_attack_damage += 10
                self.shop_message = f"Sukses membeli! Base DMG meningkat menjadi {self.player.base_attack_damage}."
                self.shop_message_color = (50, 255, 50)
            else:
                self.shop_message = "Koin Anda tidak cukup untuk membeli Pedang Tajam!"
                self.shop_message_color = (255, 50, 50)
                
        elif item_num == 2:
            cost = 200
            if self.player.score >= cost:
                if self.player.hp == self.player.max_hp:
                    self.shop_message = "HP Anda sudah penuh!"
                    self.shop_message_color = (250, 220, 50)
                else:
                    self.player.score -= cost
                    self.player.hp = self.player.max_hp
                    self.shop_message = "Sukses memulihkan HP pemain menjadi penuh!"
                    self.shop_message_color = (50, 255, 50)
            else:
                self.shop_message = "Koin Anda tidak cukup untuk membeli Ramuan Darah!"
                self.shop_message_color = (255, 50, 50)
                
        elif item_num == 3:
            cost = 400
            if self.player.score >= cost:
                if self.player.speed >= 260:
                    self.shop_message = "Kecepatan Anda sudah maksimal!"
                    self.shop_message_color = (250, 220, 50)
                else:
                    self.player.score -= cost
                    self.player.speed = 260
                    self.shop_message = "Sukses membeli! Kecepatan lari meningkat menjadi 260."
                    self.shop_message_color = (50, 255, 50)
            else:
                self.shop_message = "Koin Anda tidak cukup untuk membeli Sepatu Kilat!"
                self.shop_message_color = (255, 50, 50)

    def check_death_or_fall(self):
        if self.player.hp <= 0 and self.state != "game_over":
            self.player.hp = 0
            self.state = "game_over"
            self.auto_save()
            
        map_h = self.all_sprites.map_height if self.all_sprites.map_height > 0 else RENDER_HEIGHT
        if self.player.rect.top > map_h + 30 and self.state != "game_over":
            self.player.hp = 0
            self.state = "game_over"
            self.auto_save()

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            if dt > 0.1:
                dt = 0.1

            # 2. Event Loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    # Input khusus saat dialog aktif
                    if self.state == "dialogue":
                        self.dialogue_manager.handle_key(event.key)
                        continue
                        
                    # Pilihan tombol pada layar Game Over
                    elif self.state == "game_over":
                        if event.key == pygame.K_r:
                            self.setup_map()
                            self.state = STATE_PLAYING
                        elif event.key == pygame.K_m:
                            self.running = False
                            
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False
                    
                    elif event.key == pygame.K_b and self.state == STATE_PLAYING:
                        self.state = "shop"
                        self.shop_message = "Selamat Datang di Toko Senjata Hasumi!"
                        self.shop_message_color = (255, 255, 255)
                    elif event.key == pygame.K_b and self.state == "shop":
                        self.state = STATE_PLAYING
                            
                    elif self.state == "shop" and event.key == pygame.K_1:
                        self.buy_item(1)
                    elif self.state == "shop" and event.key == pygame.K_2:
                        self.buy_item(2)
                    elif self.state == "shop" and event.key == pygame.K_3:
                        self.buy_item(3)
                        
                    elif event.key in (pygame.K_SPACE, pygame.K_w, pygame.K_UP) and self.state == STATE_PLAYING:
                        self.player.jump()

            # 3. Game Logic & Rendering berdasarkan State
            if self.state == STATE_PLAYING:
                self.all_sprites.update(dt)
                self.check_collisions()
                self.check_death_or_fall()
                self.check_respawns()
                
                self.display_surface.fill((20, 20, 30))
                self.all_sprites.custom_draw(self.player, self.display_surface)
                self.draw_hud()
                
            elif self.state == "dialogue":
                # Jalankan dan render dialog cutscene
                self.dialogue_manager.update()
                self.display_surface.fill((20, 20, 30))
                self.all_sprites.custom_draw(self.player, self.display_surface)
                self.draw_hud()
                
            elif self.state == "shop":
                self.display_surface.fill((20, 20, 30))
                self.all_sprites.custom_draw(self.player, self.display_surface)
                self.draw_hud()
                self.draw_shop()
                
            elif self.state == "game_over":
                self.draw_game_over()

            # 4. Scaling dan Rendering ke Layar Utama
            scaled_surface = pygame.transform.scale(self.display_surface, (WINDOW_WIDTH, WINDOW_HEIGHT))
            self.screen.blit(scaled_surface, (0, 0))
            
            # Gambar kotak dialog di layar utama fisik (skala penuh 1280x720) jika aktif
            if self.state == "dialogue":
                self.dialogue_manager.draw(self.screen)
            
            pygame.display.flip()

        pygame.quit()
        sys.exit()
