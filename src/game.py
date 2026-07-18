import pygame
import sys
import math
from src.setting import (
    WINDOW_WIDTH, WINDOW_HEIGHT, DISPLAY_WIDTH, DISPLAY_HEIGHT, FRAMERATE,
    BG_COLOR, COL_GOLD, COL_ACCENT, COL_WHITE, COL_BLACK, COL_RED, COL_DARK_GRAY,
    STATE_INTRO, STATE_MENU, STATE_PLAYING, STATE_PAUSE, STATE_DIALOGUE,
    STATE_SHOP, STATE_STAGE_CLEAR, STATE_GAME_OVER, PLAYER_MAX_HP, PLAYER_ATTACK,
    MOVE_SPEED, XP_BASE
)
from src.ui import draw_text, RetroPanel, RetroButton, ProgressBar, DialogueBox

class Game:
    def __init__(self):
        # 1. Inisialisasi Pygame & Window
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Game Platformer Pixel Art 16x16")
        
        # Display internal (logical surface 400x300)
        self.display = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        
        # Clock
        self.clock = pygame.time.Clock()
        self.running = True
        
        # 2. Inisialisasi State Game
        self.current_state = STATE_INTRO
        
        # 3. Parameter Gameplay Player
        self.player_x = 40
        self.player_y = 200
        self.player_vx = 0
        self.player_vy = 0
        self.player_max_hp = PLAYER_MAX_HP
        self.player_hp = PLAYER_MAX_HP
        self.player_gold = 30
        self.player_xp = 0
        self.player_atk = PLAYER_ATTACK
        self.player_speed = MOVE_SPEED
        self.is_grounded = False
        self.invincible_timer = 0
        
        # Level Konstanta & Objek
        self.ground_y = 250
        self.npc_x = 160
        self.npc_y = 250 - 16  # Berdiri di atas tanah
        self.goal_x = 340
        self.goal_y = 250 - 24  # Bendera gol
        
        # Patroli Musuh
        self.enemy_x = 240
        self.enemy_y = 250 - 16
        self.enemy_speed = 40
        self.enemy_dir = 1
        self.enemy_patrol_min = 200
        self.enemy_patrol_max = 300
        
        # UI HUD
        self.hp_bar = ProgressBar(10, 10, 80, 8, self.player_max_hp, self.player_max_hp, COL_RED)
        self.xp_bar = ProgressBar(10, 20, 80, 5, self.player_xp, XP_BASE, COL_GOLD)
        
        # Dialogue Box
        self.dialogue_box = DialogueBox(20, DISPLAY_HEIGHT - 65, DISPLAY_WIDTH - 40, 50)
        
        # 4. Inisialisasi Tombol UI (Keyboard & Mouse compatible)
        self.menu_index = 0
        self.menu_buttons = [
            RetroButton(DISPLAY_WIDTH // 2 - 60, 120, 120, 24, "Start Game", self.start_game),
            RetroButton(DISPLAY_WIDTH // 2 - 60, 155, 120, 24, "Shop Upgrades", self.open_shop),
            RetroButton(DISPLAY_WIDTH // 2 - 60, 190, 120, 24, "Exit Game", self.exit_game)
        ]
        
        self.pause_index = 0
        self.pause_buttons = [
            RetroButton(DISPLAY_WIDTH // 2 - 60, 110, 120, 24, "Resume", self.resume_game),
            RetroButton(DISPLAY_WIDTH // 2 - 60, 145, 120, 24, "Quit to Menu", self.quit_to_menu)
        ]
        
        self.shop_index = 0
        self.shop_items = [
            {"name": "+20 Max HP (15g)", "cost": 15, "stat": "hp"},
            {"name": "+5 Attack (10g)", "cost": 10, "stat": "atk"},
            {"name": "+20 Speed (20g)", "cost": 20, "stat": "spd"}
        ]
        self.shop_buttons = [
            RetroButton(DISPLAY_WIDTH // 2 - 80, 110, 160, 22, "Upgrade HP (15g)", lambda: self.buy_upgrade(0)),
            RetroButton(DISPLAY_WIDTH // 2 - 80, 140, 160, 22, "Upgrade Atk (10g)", lambda: self.buy_upgrade(1)),
            RetroButton(DISPLAY_WIDTH // 2 - 80, 170, 160, 22, "Upgrade Spd (20g)", lambda: self.buy_upgrade(2)),
            RetroButton(DISPLAY_WIDTH // 2 - 80, 205, 160, 22, "Back to Menu", self.quit_to_menu)
        ]
        
        # State Intro Timer & Fade
        self.intro_timer = 0
        self.intro_alpha = 255
        self.intro_phase = "fade_in" # "fade_in", "hold", "fade_out"
        
    # --- AKSI BUTTONS ---
    def start_game(self):
        # Reset stats basic ketika mulai baru
        self.player_x = 40
        self.player_y = 200
        self.player_vx = 0
        self.player_vy = 0
        self.player_hp = self.player_max_hp
        self.player_xp = 0
        self.player_gold = 30
        self.current_state = STATE_PLAYING
        
    def resume_game(self):
        self.current_state = STATE_PLAYING
        
    def open_shop(self):
        self.current_state = STATE_SHOP
        self.shop_index = 0
        
    def quit_to_menu(self):
        self.current_state = STATE_MENU
        self.menu_index = 0
        
    def exit_game(self):
        self.running = False
        pygame.quit()
        sys.exit()
        
    def buy_upgrade(self, idx):
        item = self.shop_items[idx]
        if self.player_gold >= item["cost"]:
            self.player_gold -= item["cost"]
            if item["stat"] == "hp":
                self.player_max_hp += 20
                self.player_hp = self.player_max_hp  # Heal ke max setelah upgrade
                self.hp_bar.max_val = self.player_max_hp
            elif item["stat"] == "atk":
                self.player_atk += 5
            elif item["stat"] == "spd":
                self.player_speed += 20
        
    # --- LOOP UTAMA ---
    def run(self):
        while self.running:
            # Hitung delta time (dt) dalam detik
            dt = self.clock.tick(FRAMERATE) / 1000.0
            if dt > 0.1:  # Hindari lonjakan fisika jika ngelag
                dt = 0.1
                
            self.handle_events()
            self.update(dt)
            self.draw()
            
    def handle_events(self):
        # Dapatkan posisi mouse dan konversi ke koordinat display internal (400x300)
        mx, my = pygame.mouse.get_pos()
        scale_x = WINDOW_WIDTH / DISPLAY_WIDTH
        scale_y = WINDOW_HEIGHT / DISPLAY_HEIGHT
        logical_mouse_pos = (mx / scale_x, my / scale_y)
        
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.exit_game()
                
            # Input Keyboard Universal
            if event.type == pygame.KEYDOWN:
                # Toggle Pause
                if event.key == pygame.K_ESCAPE:
                    if self.current_state == STATE_PLAYING:
                        self.current_state = STATE_PAUSE
                        self.pause_index = 0
                    elif self.current_state == STATE_PAUSE:
                        self.current_state = STATE_PLAYING
                
            # Penanganan Event Berdasarkan State
            if self.current_state == STATE_INTRO:
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    # Skip intro langsung ke menu utama
                    self.current_state = STATE_MENU
                    
            elif self.current_state == STATE_MENU:
                # Hover Tombol dengan Mouse
                for i, btn in enumerate(self.menu_buttons):
                    if btn.check_hover(logical_mouse_pos):
                        self.menu_index = i
                
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_UP, pygame.K_w):
                        self.menu_index = (self.menu_index - 1) % len(self.menu_buttons)
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        self.menu_index = (self.menu_index + 1) % len(self.menu_buttons)
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        self.menu_buttons[self.menu_index].action()
                        
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for btn in self.menu_buttons:
                        if btn.is_hovered and btn.action:
                            btn.action()
                            
            elif self.current_state == STATE_PLAYING:
                if event.type == pygame.KEYDOWN:
                    # Mulai Dialog dengan NPC jika dekat
                    if event.key in (pygame.K_RETURN, pygame.K_e):
                        if abs(self.player_x - self.npc_x) < 24:
                            self.current_state = STATE_DIALOGUE
                            self.dialogue_box.start_dialogue(
                                "Kakek Bijak",
                                [
                                    "Halo, penualang cilik!",
                                    "Ada portal bendera hijau di sebelah kanan layar.",
                                    "Gunakan tombol A/D untuk jalan dan SPACE untuk melompat.",
                                    "Hindari musuh kuning yang berkeliaran itu!",
                                    "Jika kamu terluka, pergilah ke Toko Upgrade di menu utama."
                                ]
                            )
                            
            elif self.current_state == STATE_PAUSE:
                for i, btn in enumerate(self.pause_buttons):
                    if btn.check_hover(logical_mouse_pos):
                        self.pause_index = i
                        
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_UP, pygame.K_w):
                        self.pause_index = (self.pause_index - 1) % len(self.pause_buttons)
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        self.pause_index = (self.pause_index + 1) % len(self.pause_buttons)
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        self.pause_buttons[self.pause_index].action()
                        
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for btn in self.pause_buttons:
                        if btn.is_hovered and btn.action:
                            btn.action()
                            
            elif self.current_state == STATE_DIALOGUE:
                if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                    # Cek key untuk lanjut text dialog
                    if event.type == pygame.MOUSEBUTTONDOWN or event.key in (pygame.K_SPACE, pygame.K_RETURN):
                        has_more = self.dialogue_box.next_line()
                        if not has_more:
                            self.current_state = STATE_PLAYING
                            
            elif self.current_state == STATE_SHOP:
                for i, btn in enumerate(self.shop_buttons):
                    if btn.check_hover(logical_mouse_pos):
                        self.shop_index = i
                        
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_UP, pygame.K_w):
                        self.shop_index = (self.shop_index - 1) % len(self.shop_buttons)
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        self.shop_index = (self.shop_index + 1) % len(self.shop_buttons)
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        self.shop_buttons[self.shop_index].action()
                    elif event.key == pygame.K_ESCAPE:
                        self.quit_to_menu()
                        
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for btn in self.shop_buttons:
                        if btn.is_hovered and btn.action:
                            btn.action()
                            
            elif self.current_state in (STATE_STAGE_CLEAR, STATE_GAME_OVER):
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        if self.current_state == STATE_STAGE_CLEAR:
                            # Lanjut main
                            self.start_game()
                        else:
                            # Restart setelah game over
                            self.start_game()
                    elif event.key == pygame.K_ESCAPE:
                        self.quit_to_menu()

    def update(self, dt):
        if self.current_state == STATE_INTRO:
            self.intro_timer += dt
            if self.intro_phase == "fade_in":
                self.intro_alpha -= int(300 * dt)
                if self.intro_alpha <= 0:
                    self.intro_alpha = 0
                    self.intro_phase = "hold"
                    self.intro_timer = 0
            elif self.intro_phase == "hold":
                if self.intro_timer > 1.5:  # tahan 1.5 detik
                    self.intro_phase = "fade_out"
            elif self.intro_phase == "fade_out":
                self.intro_alpha += int(300 * dt)
                if self.intro_alpha >= 255:
                    self.intro_alpha = 255
                    self.current_state = STATE_MENU
                    
        elif self.current_state == STATE_PLAYING:
            self.update_physics(dt)
            
        elif self.current_state == STATE_DIALOGUE:
            self.dialogue_box.update()

    def update_physics(self, dt):
        # 1. Update Cooldown Invincibility Player
        if self.invincible_timer > 0:
            self.invincible_timer -= dt
            
        # 2. Deteksi Key Pergerakan Player
        keys = pygame.key.get_pressed()
        self.player_vx = 0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.player_vx = -self.player_speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.player_vx = self.player_speed
            
        # Lompat (Jump)
        if (keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]) and self.is_grounded:
            self.player_vy = -180  # Kekuatan lompatan
            self.is_grounded = False
            
        # Gravitasi
        self.player_vy += 500 * dt  # Kecepatan gravitasi px/s^2
        if self.player_vy > 300:     # Limit fall speed
            self.player_vy = 300
            
        # 3. Update Posisi Player & Batas Layar
        self.player_x += self.player_vx * dt
        self.player_y += self.player_vy * dt
        
        # Batasi agar player tidak keluar layar horizontal
        if self.player_x < 0:
            self.player_x = 0
        elif self.player_x > DISPLAY_WIDTH - 16:
            self.player_x = DISPLAY_WIDTH - 16
            
        # Deteksi tabrakan tanah (sederhana)
        if self.player_y + 16 >= self.ground_y:
            self.player_y = self.ground_y - 16
            self.player_vy = 0
            self.is_grounded = True
            
        # 4. Update Musuh (Patroli)
        self.enemy_x += self.enemy_speed * self.enemy_dir * dt
        if self.enemy_x >= self.enemy_patrol_max:
            self.enemy_x = self.enemy_patrol_max
            self.enemy_dir = -1
        elif self.enemy_x <= self.enemy_patrol_min:
            self.enemy_x = self.enemy_patrol_min
            self.enemy_dir = 1
            
        # 5. Deteksi Tabrakan Player dengan Musuh
        player_rect = pygame.Rect(self.player_x, self.player_y, 16, 16)
        enemy_rect = pygame.Rect(self.enemy_x, self.enemy_y, 16, 16)
        
        if player_rect.colliderect(enemy_rect) and self.invincible_timer <= 0:
            # Player kena damage
            self.player_hp -= 20
            self.invincible_timer = 1.0  # 1 detik invincibility
            # Sedikit dorongan terpental (knockback)
            self.player_vy = -80
            self.player_vx = -self.enemy_dir * 100
            
            if self.player_hp <= 0:
                self.player_hp = 0
                self.current_state = STATE_GAME_OVER
                
        # 6. Deteksi Tabrakan Player dengan Bendera Gol (Goal)
        goal_rect = pygame.Rect(self.goal_x, self.goal_y, 16, 24)
        if player_rect.colliderect(goal_rect):
            self.player_gold += 25
            self.player_xp += 50
            self.current_state = STATE_STAGE_CLEAR

    # --- RENDERING STATE ---
    def draw(self):
        # Bersihkan display internal
        self.display.fill(BG_COLOR)
        
        # Gambar sesuai State saat ini
        if self.current_state == STATE_INTRO:
            self.draw_intro()
        elif self.current_state == STATE_MENU:
            self.draw_menu()
        elif self.current_state == STATE_PLAYING:
            self.draw_playing()
        elif self.current_state == STATE_PAUSE:
            # Gambar playing di latar belakang terlebih dahulu
            self.draw_playing()
            self.draw_pause()
        elif self.current_state == STATE_DIALOGUE:
            self.draw_playing()
            self.draw_dialogue()
        elif self.current_state == STATE_SHOP:
            self.draw_shop()
        elif self.current_state == STATE_STAGE_CLEAR:
            self.draw_playing()
            self.draw_stage_clear()
        elif self.current_state == STATE_GAME_OVER:
            self.draw_playing()
            self.draw_game_over()
            
        # Lakukan Scale-Up dari display (400x300) ke screen utama (800x600)
        scaled_display = pygame.transform.scale(self.display, self.screen.get_size())
        self.screen.blit(scaled_display, (0, 0))
        
        # Update layar fisik
        pygame.display.update()

    def draw_intro(self):
        self.display.fill(COL_BLACK)
        # Menampilkan teks logo pembuat
        draw_text(self.display, "ANTIGRAVITY DEV", DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2 - 10, size=18, color=COL_ACCENT, center=True)
        draw_text(self.display, "PRESENTS", DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2 + 10, size=12, color=COL_WHITE, center=True)
        
        # Lapisan penutup hitam untuk efek fade in/out
        fade_surface = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        fade_surface.fill(COL_BLACK)
        fade_surface.set_alpha(self.intro_alpha)
        self.display.blit(fade_surface, (0, 0))

    def draw_menu(self):
        # Background Hiasan Langit & Bukit Sederhana
        pygame.draw.rect(self.display, (135, 206, 235), (0, 0, DISPLAY_WIDTH, 200))  # Langit
        pygame.draw.rect(self.display, (100, 200, 100), (0, 200, DISPLAY_WIDTH, DISPLAY_HEIGHT - 200))  # Bukit
        
        # Efek Tulisan Mengapung (Floating)
        float_y = DISPLAY_HEIGHT // 2 - 70 + int(math.sin(pygame.time.get_ticks() / 200) * 4)
        
        # Bayangan Teks Judul
        draw_text(self.display, "PIXEL PLATFORMER", DISPLAY_WIDTH // 2 + 2, float_y + 2, size=24, color=COL_BLACK, center=True)
        draw_text(self.display, "PIXEL PLATFORMER", DISPLAY_WIDTH // 2, float_y, size=24, color=COL_GOLD, center=True)
        
        # Render Tombol Menu
        for i, btn in enumerate(self.menu_buttons):
            btn.draw(self.display, is_selected=(i == self.menu_index))
            
        # Petunjuk Kontrol
        draw_text(self.display, "Arah / WASD: Pilih | ENTER / Klik: OK", DISPLAY_WIDTH // 2, DISPLAY_HEIGHT - 20, size=12, color=COL_BLACK, center=True)

    def draw_playing(self):
        # 1. Background langit biru cerah
        self.display.fill((135, 206, 235))
        
        # 2. Gambar Tanah (Ground Grid 16x16px sederhana)
        pygame.draw.rect(self.display, (101, 67, 33), (0, self.ground_y, DISPLAY_WIDTH, DISPLAY_HEIGHT - self.ground_y))  # Tanah cokelat
        pygame.draw.rect(self.display, (34, 139, 34), (0, self.ground_y, DISPLAY_WIDTH, 4))  # Rumput hijau atas tanah
        
        # Grid visual 16px untuk memperjelas skala pixel art
        for x in range(0, DISPLAY_WIDTH, 16):
            pygame.draw.line(self.display, (90, 60, 30), (x, self.ground_y + 4), (x, DISPLAY_HEIGHT), 1)
            
        # 3. Gambar NPC (Kotak biru kecil dengan wajah sederhana)
        npc_rect = pygame.Rect(self.npc_x, self.npc_y, 16, 16)
        pygame.draw.rect(self.display, (50, 100, 240), npc_rect)  # Badan NPC
        pygame.draw.rect(self.display, COL_WHITE, (self.npc_x + 3, self.npc_y + 3, 2, 2))  # Mata kiri
        pygame.draw.rect(self.display, COL_WHITE, (self.npc_x + 9, self.npc_y + 3, 2, 2))  # Mata kanan
        
        # Petunjuk Dialog jika dekat
        if abs(self.player_x - self.npc_x) < 24:
            draw_text(self.display, "ENTER untuk bicara", self.npc_x - 36, self.npc_y - 12, size=10, color=COL_WHITE)
            
        # 4. Gambar Goal (Tiang kayu dan Bendera Merah bergelombang)
        pygame.draw.rect(self.display, (150, 75, 0), (self.goal_x + 2, self.goal_y, 2, 24))  # Tiang
        # Animasi bendera bergelombang
        wave_offset = int(math.sin(pygame.time.get_ticks() / 150) * 2)
        flag_points = [
            (self.goal_x + 4, self.goal_y),
            (self.goal_x + 16 + wave_offset, self.goal_y + 4),
            (self.goal_x + 4, self.goal_y + 8)
        ]
        pygame.draw.polygon(self.display, COL_RED, flag_points)
        draw_text(self.display, "GOAL", self.goal_x - 6, self.goal_y - 10, size=10, color=COL_WHITE)

        # 5. Gambar Patroli Musuh (Kotak kuning dengan mata merah)
        enemy_rect = pygame.Rect(self.enemy_x, self.enemy_y, 16, 16)
        pygame.draw.rect(self.display, (220, 200, 50), enemy_rect)  # Badan Musuh
        pygame.draw.rect(self.display, COL_RED, (self.enemy_x + (3 if self.enemy_dir == -1 else 10), self.enemy_y + 4, 3, 3))  # Mata merah sesuai arah jalan
        
        # 6. Gambar Player (Kotak merah dengan mata)
        # Efek kedip (flickering) jika invincible
        if self.invincible_timer <= 0 or (pygame.time.get_ticks() // 100) % 2 == 0:
            player_rect = pygame.Rect(self.player_x, self.player_y, 16, 16)
            pygame.draw.rect(self.display, COL_RED, player_rect)
            # Mata mengarah ke arah jalan
            eye_offset = 11 if self.player_vx >= 0 else 2
            pygame.draw.rect(self.display, COL_WHITE, (self.player_x + eye_offset, self.player_y + 3, 3, 3))
            pygame.draw.rect(self.display, COL_BLACK, (self.player_x + eye_offset + (1 if self.player_vx >= 0 else 0), self.player_y + 4, 1, 1))

        # 7. Gambar HUD
        # Box HUD background
        hud_bg = RetroPanel(4, 4, 140, 32, bg_color=(20, 20, 20), border_color=COL_WHITE)
        hud_bg.draw(self.display)
        
        self.hp_bar.draw(self.display, self.player_hp)
        self.xp_bar.draw(self.display, self.player_xp)
        
        draw_text(self.display, f"HP: {int(self.player_hp)}/{self.player_max_hp}", 96, 8, size=9, color=COL_WHITE)
        draw_text(self.display, f"Gold: {self.player_gold}g", 96, 18, size=9, color=COL_GOLD)

    def draw_pause(self):
        # Overlay abu-abu transparan di latar belakang
        overlay = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        overlay.fill(COL_BLACK)
        overlay.set_alpha(150)
        self.display.blit(overlay, (0, 0))
        
        # Panel Pause Card
        panel = RetroPanel(DISPLAY_WIDTH // 2 - 75, DISPLAY_HEIGHT // 2 - 60, 150, 120)
        panel.draw(self.display)
        
        draw_text(self.display, "PAUSED", DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2 - 40, size=18, color=COL_GOLD, center=True)
        
        # Render Tombol Pause
        for i, btn in enumerate(self.pause_buttons):
            btn.draw(self.display, is_selected=(i == self.pause_index))

    def draw_dialogue(self):
        # Update dan Gambar Dialog Box langsung di canvas display
        self.dialogue_box.draw(self.display)

    def draw_shop(self):
        self.display.fill((45, 30, 25))  # Latar belakang interior kayu tua
        
        # Panel Shop Utama
        panel = RetroPanel(20, 20, DISPLAY_WIDTH - 40, DISPLAY_HEIGHT - 40)
        panel.draw(self.display)
        
        draw_text(self.display, "OLD MAN'S UPGRADE SHOP", DISPLAY_WIDTH // 2, 35, size=16, color=COL_GOLD, center=True)
        
        # Informasi Statistik Player saat ini
        stats_y = 60
        draw_text(self.display, f"Gold Kamu: {self.player_gold}g", DISPLAY_WIDTH // 2 - 120, stats_y, size=11, color=COL_GOLD)
        draw_text(self.display, f"STAT: HP {self.player_max_hp} | Atk {self.player_atk} | Spd {self.player_speed}", DISPLAY_WIDTH // 2 - 120, stats_y + 12, size=11, color=COL_WHITE)
        
        # Render Tombol Upgrade
        for i, btn in enumerate(self.shop_buttons):
            btn.draw(self.display, is_selected=(i == self.shop_index))
            
        # Catatan/Keterangan di bagian bawah
        draw_text(self.display, "Tekan ESC untuk kembali ke Menu Utama", DISPLAY_WIDTH // 2, DISPLAY_HEIGHT - 35, size=10, color=COL_ACCENT, center=True)

    def draw_stage_clear(self):
        # Overlay transparan hijau gelap
        overlay = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        overlay.fill((20, 80, 20))
        overlay.set_alpha(180)
        self.display.blit(overlay, (0, 0))
        
        panel = RetroPanel(DISPLAY_WIDTH // 2 - 90, DISPLAY_HEIGHT // 2 - 50, 180, 100)
        panel.draw(self.display)
        
        draw_text(self.display, "STAGE CLEAR!", DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2 - 35, size=18, color=COL_GOLD, center=True)
        draw_text(self.display, "Hadiah: +25 Gold & +50 XP", DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2 - 5, size=11, color=COL_WHITE, center=True)
        
        # Animasi Tekan Enter berkedip
        if (pygame.time.get_ticks() // 500) % 2 == 0:
            draw_text(self.display, "Tekan ENTER untuk Lanjut", DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2 + 25, size=11, color=COL_ACCENT, center=True)

    def draw_game_over(self):
        # Overlay transparan merah gelap
        overlay = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        overlay.fill((80, 20, 20))
        overlay.set_alpha(180)
        self.display.blit(overlay, (0, 0))
        
        panel = RetroPanel(DISPLAY_WIDTH // 2 - 90, DISPLAY_HEIGHT // 2 - 50, 180, 100)
        panel.draw(self.display)
        
        draw_text(self.display, "GAME OVER", DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2 - 35, size=18, color=COL_RED, center=True)
        draw_text(self.display, "Kamu dikalahkan musuh!", DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2 - 5, size=11, color=COL_WHITE, center=True)
        
        # Animasi Tekan Enter berkedip
        if (pygame.time.get_ticks() // 500) % 2 == 0:
            draw_text(self.display, "Tekan ENTER untuk Retry", DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2 + 25, size=11, color=COL_ACCENT, center=True)
