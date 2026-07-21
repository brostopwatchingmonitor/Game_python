from settings import * 
from sprites import *
from player import Player
from pathlib import Path
from groups import AllSprites
from support import *
from timer import Timer
from random import randint

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Platformer')
        self.clock = pygame.time.Clock()
        self.running = True

        # groups 
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()

        # UI, Dialogue & State
        from dialogue import DialogueManager
        from ui import UI as GameUI
        from game_state import GameState
        from stage import StageManager
        from background import Background
        from map import StageMap
        
        self.state = GameState()
        self.stage_mgr = StageManager()
        self.stage_map = StageMap()
        self.background = Background()
        
        self.dialogue_manager = DialogueManager()
        self.ui = GameUI()
        self.player = None
        self.boss = None
        self.score = 0
        self.loaded_save_data = None
        self.exit_rect = None

        # Mulai dengan state INTRO typewriter
        self.state.go_intro()
        self.load_assets()

    def create_bullet(self, pos, direction):
        if isinstance(direction, pygame.Vector2):
            Bullet(self.bullet_surf, pos, direction, (self.all_sprites, self.bullet_sprites), mode="boss")
        else:
            x = pos[0] + direction * 34
            bullet_pos = (x, pos[1])
            Bullet(self.bullet_surf, bullet_pos, direction, (self.all_sprites, self.bullet_sprites), mode="default")
        Fire(self.fire_surf, pos, self.all_sprites, self.player)
 
    def load_assets(self):
        self.player_frames = import_folder('..', 'images', 'player')
        self.bullet_surf = import_image('..', 'images', 'gun', 'bullet')
        self.fire_surf = import_image('..', 'images', 'gun', 'fire')

    def spawn_enemy(self):
        import random
        from enemy import BaseEnemy, ENEMY_TYPES
        
        st = self.stage_mgr.current
        if not st or st.has_boss:
            return

        enemy_pool = st.enemy_pool
        enemy_name = random.choice(enemy_pool)
        
        # Spawn from the designated TMX spawn points first if available, otherwise spawn around player
        if getattr(self, 'stage_enemy_spawn_points', None):
            spawn_x, spawn_y = random.choice(self.stage_enemy_spawn_points)
        else:
            spawn_x = self.player.rect.centerx + WINDOW_WIDTH // 2 + random.randint(50, 200)
            if spawn_x > self.map_width - 100:
                spawn_x = self.player.rect.centerx - WINDOW_WIDTH // 2 - random.randint(50, 200)
            spawn_x = max(50, min(self.map_width - 100, spawn_x))
            
            # Determine Y spawn coordinates
            if enemy_name == "Crab":
                spawn_y = self.map_height - 120
            else:
                spawn_y = random.randint(100, self.map_height - 180)
            
        BaseEnemy((spawn_x, spawn_y), enemy_name, (self.all_sprites, self.enemy_sprites), self.collision_sprites, self.player)

    def start_stage(self, stage_idx):
        # Bersihkan sprite lama sebelum memuat stage baru
        self.all_sprites.empty()
        self.collision_sprites.empty()
        self.bullet_sprites.empty()
        self.enemy_sprites.empty()
        
        # Reset progress stage jika diulang/dimulai
        st = self.stage_mgr.current
        if st:
            st.kill_count   = 0
            st.boss_spawned = False
            st.boss_dead    = False
            st.completed    = False
        
        self.boss = None
        self.exit_rect = None
        self.stage_enemy_spawn_points = []

        # Reset continuous enemy spawning variables
        self.enemy_spawn_timer = 0.0
        if st:
            self.enemy_spawn_cooldown = 200.0 / st.spawn_rate if st.spawn_rate > 0 else 5.0
        else:
            self.enemy_spawn_cooldown = 2.0

        # Load stage from STAGES configuration
        from stage import STAGES
        stage_cfg = STAGES.get(stage_idx + 1)
        if not stage_cfg:
            print(f"Error: Stage index {stage_idx} not found in configuration.")
            return

        # Switch camera mode
        self.all_sprites.set_camera_mode(stage_cfg["camera"])

        from pytmx.util_pygame import load_pygame
        tmx_path = join(BASE_DIR, '..', stage_cfg["map"])
        tmx_data = load_pygame(tmx_path)
        
        tile_scale = stage_cfg.get("tile_scale", 1.0)
        scaled_tilewidth = int(tmx_data.tilewidth * tile_scale)
        scaled_tileheight = int(tmx_data.tileheight * tile_scale)

        self.map_width = tmx_data.width * scaled_tilewidth
        self.map_height = tmx_data.height * scaled_tileheight
        
        # Build physical map
        for layer in tmx_data.visible_layers:
            if hasattr(layer, 'data'):
                for x, y, surf in layer.tiles():
                    pos = (x * scaled_tilewidth, y * scaled_tileheight)
                    scaled_surf = pygame.transform.scale(surf, (scaled_tilewidth, scaled_tileheight))
                    if layer.name in ('ground', 'wood', 'wall'):
                        Sprites(pos, scaled_surf, (self.all_sprites, self.collision_sprites))
                    else:
                        Sprites(pos, scaled_surf, self.all_sprites)

        # Find Object positions
        player_pos = (100, 100)
        boss_pos = (self.map_width // 2, self.map_height // 2)

        for obj in tmx_data.objects:
            obj_x = obj.x * tile_scale
            obj_y = obj.y * tile_scale
            obj_w = obj.width * tile_scale
            obj_h = obj.height * tile_scale

            if obj.name == 'player':
                player_pos = (obj_x, obj_y)
            elif obj.name == 'exit':
                self.exit_rect = pygame.Rect(obj_x, obj_y, obj_w, obj_h)
            elif obj.name == 'boss':
                boss_pos = (obj_x, obj_y)
            elif obj.name == 'enemy':
                self.stage_enemy_spawn_points.append((obj_x, obj_y))

        # Re-spawn player di posisi awal stage baru
        self.player = Player(player_pos, self.all_sprites, self.collision_sprites, self.player_frames, self.create_bullet)
        self.player.movement_mode = stage_cfg["camera"]

        # Spawn boss if Stage 3, otherwise spawn normal TMX enemies
        if stage_cfg.get("has_boss"):
            from enemy import BossEnemy
            self.boss = BossEnemy(boss_pos, "Lord HyperEnd", (self.all_sprites, self.enemy_sprites), self.collision_sprites, self.player)
            if st:
                st.boss_spawned = True
        else:
            # Spawn initial enemies from spawn points
            from enemy import BaseEnemy
            import random
            enemy_types_pool = stage_cfg.get("enemy_pool", ["Crab", "Jellyfish"])
            for pt in self.stage_enemy_spawn_points:
                enemy_type = random.choice(enemy_types_pool)
                BaseEnemy(pt, enemy_type, (self.all_sprites, self.enemy_sprites), self.collision_sprites, self.player)

        # Apply save data if loaded
        if getattr(self, 'loaded_save_data', None) is not None:
            from save_manager import SaveManager
            SaveManager.apply(self.loaded_save_data, self.player, None)
            self.score = self.loaded_save_data.get("score", 0)
            self.loaded_save_data = None

        # Set map dimensions
        self.player.map_width = self.map_width
        self.player.map_height = self.map_height
        self.all_sprites.map_width = self.map_width
        self.all_sprites.map_height = self.map_height

    def run(self):
        while self.running:
            dt = self.clock.tick(FRAMERATE) / 1000 

            # ── 1. Event Handling per State ──
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False 
                elif event.type == pygame.KEYDOWN:
                    # Intro State
                    if self.state.is_intro:
                        if event.key == pygame.K_RETURN:
                            if self.ui._intro_done:
                                self.state.go_menu()
                            else:
                                self.ui._intro_done = True
                                self.ui._intro_line = len(self.ui.INTRO_LINES)
                    
                    # Menu Utama
                    elif self.state.is_menu:
                        if event.key == pygame.K_RETURN:
                            from save_manager import SaveManager
                            SaveManager.delete()
                            self.state.go_map()
                        elif event.key == pygame.K_l:
                            from save_manager import SaveManager
                            save_data = SaveManager.load()
                            if save_data:
                                self.stage_mgr.current_idx = save_data.get("stage", 0)
                                self.loaded_save_data = save_data
                                self.state.go_map()
                            else:
                                self.state.go_map()
                        elif event.key == pygame.K_ESCAPE:
                            self.running = False

                    # Layar Peta (Stage Select)
                    elif self.state.is_map:
                        if event.key == pygame.K_b or event.key == pygame.K_ESCAPE:
                            self.state.go_menu()
                        else:
                            from map import StageMap
                            selected = self.stage_map.handle_key(event.key, self.stage_mgr)
                            if selected is not None:
                                self.start_stage(selected)
                                
                                def on_dialogue_complete():
                                    self.state.go_playing()
                                
                                self.dialogue_manager.start_cutscene(f"intro_stage_{selected}", 
                                    on_complete_callback=on_dialogue_complete)
                                self.state.go_dialogue()

                    # Layar Dialog Cutscene
                    elif self.state.is_dialogue:
                        self.dialogue_manager.handle_key(event.key)

                    # Layar Game Over
                    elif self.state.is_game_over:
                        if event.key == pygame.K_r:
                            self.score = 0
                            self.start_stage(self.stage_mgr.current_idx)
                            self.state.go_playing()
                        elif event.key == pygame.K_m:
                            self.state.go_menu()

                    # Layar Win
                    elif self.state.is_win:
                        if event.key == pygame.K_r or event.key == pygame.K_RETURN:
                            self.score = 0
                            self.stage_mgr.reset()
                            self.state.go_menu()

            # ── 2. Update Logic per State ──
            if self.state.is_intro:
                self.ui.update_intro()
            elif self.state.is_dialogue:
                self.dialogue_manager.update()
            elif self.state.is_playing:
                self.all_sprites.update(dt)
                self.background.update()

                # Pass camera offset to player
                if self.player:
                    self.player.camera_offset = self.all_sprites.offset

                # Spawning musuh berkelanjutan secara real-time
                if self.stage_mgr.current and not self.stage_mgr.current.has_boss:
                    self.enemy_spawn_timer += dt
                    if self.enemy_spawn_timer >= self.enemy_spawn_cooldown:
                        self.enemy_spawn_timer = 0.0
                        self.spawn_enemy()
                        self.enemy_spawn_cooldown = max(2.5, self.enemy_spawn_cooldown - 0.05)

                # Collision check
                # 1. Peluru player menabrak musuh
                for bullet in self.bullet_sprites:
                    hit_enemies = pygame.sprite.spritecollide(bullet, self.enemy_sprites, False)
                    if hit_enemies:
                        bullet.kill()
                        for enemy in hit_enemies:
                            if hasattr(enemy, 'take_damage'):
                                enemy.take_damage(self.player.attack)
                                if enemy.hp <= 0:
                                    self.score += 100
                                    if hasattr(enemy, 'xp'):
                                        stage_idx = self.stage_mgr.current_idx if self.stage_mgr else 0
                                        self.player.gain_xp(enemy.xp, stage_idx)
                                    if self.stage_mgr.current:
                                        self.stage_mgr.current.register_kill()

                # 2. Musuh menabrak Player
                hit_player_enemies = pygame.sprite.spritecollide(self.player, self.enemy_sprites, False)
                if hit_player_enemies and not self.player.invincible:
                    for enemy in hit_player_enemies:
                        self.player.hp = max(0, self.player.hp - (enemy.damage * 0.05))
                        if self.player.hp <= 0:
                            print("Player mati!")
                            self.state.go_game_over()

                # 3. Cek Stage Clear / Progress ke stage selanjutnya
                if self.stage_mgr.current:
                    # Check if normal stage goal is met (but don't transition automatically until exit collision)
                    if not self.stage_mgr.current.completed and self.stage_mgr.current.kill_count >= self.stage_mgr.current.kill_target:
                        self.stage_mgr.current.completed = True
                        print("Mission objective complete! Proceed to the exit portal.")
                    
                    # Check if exit portal reached for Stage 1 & 2
                    if self.stage_mgr.current.completed and self.exit_rect and self.player.rect.colliderect(self.exit_rect):
                        current_idx = self.stage_mgr.current_idx
                        clear_key = f"clear_stage_{current_idx}"
                        
                        def on_clear_dialogue_complete():
                            if self.stage_mgr.is_last_stage:
                                def on_win_ending_complete():
                                    self.state.go_win()
                                self.dialogue_manager.start_cutscene("win_ending", on_complete_callback=on_win_ending_complete)
                                self.state.go_dialogue()
                            else:
                                self.stage_mgr.advance()
                                next_idx = self.stage_mgr.current_idx
                                self.start_stage(next_idx)
                                
                                # Auto-save game state
                                from save_manager import SaveManager
                                SaveManager.save(self.player, next_idx, self.score, 0, [])
                                
                                def on_next_intro_complete():
                                    self.state.go_playing()
                                self.dialogue_manager.start_cutscene(f"intro_stage_{next_idx}", on_complete_callback=on_next_intro_complete)
                                self.state.go_dialogue()
                                
                        self.dialogue_manager.start_cutscene(clear_key, on_complete_callback=on_clear_dialogue_complete)
                        self.state.go_dialogue()
                    
                    # Check if boss defeated in Stage 3
                    if self.boss and not self.boss.alive() and not self.stage_mgr.current.completed:
                        self.stage_mgr.current.completed = True
                        self.stage_mgr.current.boss_dead = True
                        
                        current_idx = self.stage_mgr.current_idx
                        clear_key = f"clear_stage_{current_idx}"
                        
                        def on_clear_dialogue_complete():
                            def on_win_ending_complete():
                                self.state.go_win()
                            self.dialogue_manager.start_cutscene("win_ending", on_complete_callback=on_win_ending_complete)
                            self.state.go_dialogue()
                            
                        self.dialogue_manager.start_cutscene(clear_key, on_complete_callback=on_clear_dialogue_complete)
                        self.state.go_dialogue()

            # ── 3. Render per State ──
            if self.state.is_intro:
                self.display_surface.fill((0, 5, 15))
                self.ui.draw_intro(self.display_surface)
            elif self.state.is_menu:
                import os
                from save_manager import SAVE_PATH
                has_save = os.path.exists(SAVE_PATH)
                self.ui.draw_menu(self.display_surface, has_save=has_save)
            elif self.state.is_map:
                self.stage_map.draw(self.display_surface, self.stage_mgr)
            elif self.state.is_playing:
                if self.player:
                    self.background.draw(self.display_surface, self.player.rect.centerx - WINDOW_WIDTH // 2)
                    self.all_sprites.draw(self.player.rect.center)
                    self.ui.draw_hud(self.display_surface, self.player, score=self.score, stage=self.stage_mgr.current, skill_manager=None)
                    # Draw boss health bar if boss is active
                    if self.boss and self.boss.alive():
                        self.ui.draw_boss_bar(self.display_surface, self.boss)
                else:
                    self.display_surface.fill((0, 5, 15))
            elif self.state.is_dialogue:
                if self.player:
                    self.background.draw(self.display_surface, self.player.rect.centerx - WINDOW_WIDTH // 2)
                    self.all_sprites.draw(self.player.rect.center)
                else:
                    self.display_surface.fill((0, 5, 15))
                self.dialogue_manager.draw(self.display_surface)
            elif self.state.is_game_over:
                self.ui.draw_game_over(self.display_surface, score=self.score, kill_count=self.stage_mgr.current.kill_count if self.stage_mgr.current else 0, level=self.player.level if self.player else 1)
            elif self.state.is_win:
                self.ui.draw_win(self.display_surface, score=self.score, kill_count=self.stage_mgr.current.kill_count if self.stage_mgr.current else 0, level=self.player.level if self.player else 1)

            pygame.display.update()
        
        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run() 