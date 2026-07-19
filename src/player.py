import pygame
from sprites import AnimatedSprites
from timer import Timer
from stage import *

class Player(AnimatedSprites):
    def __init__(self, pos, groups, collision_sprites, frames, create_bullet):
        # Inisialisasi frame & animasi (list atau dict)
        self.animations = None
        if isinstance(frames, dict):
            self.animations = frames
            self.frames = self.animations.get('idle', [])
        else:
            self.frames = frames

        super().__init__(pos, self.frames, groups)
        self.flip = False
        self.create_bullet = create_bullet        # Jika frame kosong, tentukan rect fallback. Jika berisi, set rect 40x80 dengan image_offset alignment
        if not self.frames:
            self.rect = pygame.Rect(pos[0], pos[1], 32, 48)
            self.image_offset = pygame.Vector2(0, 0)
        else:
            self.rect = pygame.Rect(pos[0], pos[1], 40, 80)
            self.image_offset = pygame.Vector2(-44, -18)
        # movement & collision
        self.direction = pygame.Vector2()
        self.collision_sprites = collision_sprites
        self.speed = 400
        self.gravity = 40
        self.on_floor = False
        
        # New movement mode: 'default' (platformer) or 'boss' (top-down)
        self.movement_mode = "default"
        self.camera_offset = pygame.Vector2()

        # Stats RPG untuk UI
        self.hp = 100
        self.max_hp = 100
        self.wp = 60         # stamina / willpower
        self.max_wp = 60
        self.level = 1
        self.gold = 0
        self.xp = 0
        self.xp_to_lv = 100
        self.attack = 30
        self._wp_exhausted = False

        # Dash mechanics
        self.dashing = False
        self.dash_timer = Timer(200) # durasi dash 200ms
        self.dash_cooldown = Timer(800) # cd dash 800ms
        self.dash_direction = 0
        self.dash_speed = 900
        self.invincible = False      # Status kebal saat dash

        # timer
        self.shoot_timer = Timer(500)

    def gain_xp(self, amount, stage_idx=0):
        self.xp += amount
        if self.xp >= self.xp_to_lv:
            self.xp -= self.xp_to_lv
            self.level += 1
            if stage_idx == 0:
                self.xp_to_lv = int(self.xp_to_lv * 1.25)
            elif stage_idx == 1:
                self.xp_to_lv = int(self.xp_to_lv * 1.35)
            elif stage_idx == 2:
                self.xp_to_lv = int(self.xp_to_lv * 1.50)
            else:
                self.xp_to_lv = int(self.xp_to_lv * 1.60)
            
            # Tiap level naik:
            self.max_hp += 15        # Max HP bertambah +15
            self.hp = self.max_hp    # Darah (HP) kembali penuh
            self.attack += 5         # Damage (Attack) bertambah +5
            self.max_wp += 5         # Max stamina (WP) bertambah +5
            self.wp = self.max_wp
            print(f"LEVEL UP! Level {self.level} - HP Penuh, Damage +5, MaxHP +15! {self.xp_to_lv}")
    
    def input(self):
        # Jika sedang dash, abaikan input gerakan biasa
        if self.dashing:
            return

        keys = pygame.key.get_pressed()
        
        if self.movement_mode == "boss":
            # 8-directional movement in Top-Down mode
            self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
            self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
            if self.direction.length() > 0:
                self.direction = self.direction.normalize()
        else:
            # Platformer movement
            self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
            
            # Lompat mengonsumsi 15 Stamina (WP)
            if keys[pygame.K_SPACE] and self.on_floor:
                if self.wp >= 15:
                    self.direction.y = -20
                    self.wp -= 15
                else:
                    print("Stamina tidak cukup untuk melompat!")

        # Mouse Click Action: Klik Kiri = Tembak, Klik Kanan = Dash (Dash hanya di Platformer)
        mouse_buttons = pygame.mouse.get_pressed()
        
        # Tembak
        if mouse_buttons[0] and not self.shoot_timer:
            if self.movement_mode == "boss":
                # Aim at mouse position relative to player screen coordinates
                mouse_pos = pygame.mouse.get_pos()
                player_screen_center = pygame.Vector2(self.rect.center) + self.camera_offset
                direction_vec = pygame.Vector2(mouse_pos) - player_screen_center
                if direction_vec.length() == 0:
                    direction_vec = pygame.Vector2(1, 0)
                self.create_bullet(self.rect.center, direction_vec)
            else:
                self.create_bullet(self.rect.center, -1 if self.flip else 1)
            self.shoot_timer.activate()
            
        # Dash menggunakan Klik Kanan (mengonsumsi 20 Stamina) - Hanya Platformer
        if self.movement_mode != "boss" and mouse_buttons[2] and not self.dash_timer and not self.dash_cooldown and self.wp >= 20:
            self.dash_direction = self.direction.x if self.direction.x != 0 else (-1 if self.flip else 1)
            self.dashing = True
            self.invincible = True
            self.wp -= 20
            self.dash_timer.activate()
            self.dash_cooldown.activate()

    def move(self, dt):
        if self.movement_mode == "boss":
            # Top-down free movement
            self.rect.x += self.direction.x * self.speed * dt
            self.collision('horizontal')
            self.rect.y += self.direction.y * self.speed * dt
            self.collision('vertical')
        else:
            # Platformer movement
            if self.dashing:
                # Gerakan Dash cepat secara horizontal
                self.rect.x += self.dash_direction * self.dash_speed * dt
                self.collision('horizontal')
                self.direction.y = 0 # Abaikan gravitasi saat dash
            else:
                # Gerakan biasa
                self.rect.x += self.direction.x * self.speed * dt
                self.collision('horizontal')
                
                # vertical movement
                self.direction.y += self.gravity * dt
                self.rect.y += self.direction.y
                self.collision('vertical')

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if direction == 'horizontal':
                    if self.direction.x > 0 or (self.dashing and self.dash_direction > 0):
                        self.rect.right = sprite.rect.left
                    elif self.direction.x < 0 or (self.dashing and self.dash_direction < 0):
                        self.rect.left = sprite.rect.right
                elif direction == 'vertical':
                    if self.movement_mode == "boss":
                        if self.direction.y > 0:
                            self.rect.bottom = sprite.rect.top
                        elif self.direction.y < 0:
                            self.rect.top = sprite.rect.bottom
                    else:
                        if self.direction.y > 0: # moving down
                            self.rect.bottom = sprite.rect.top
                            self.direction.y = 0
                        elif self.direction.y < 0: # moving up
                            self.rect.top = sprite.rect.bottom
                            self.direction.y = 0

    def check_floor(self):
        if self.movement_mode == "boss":
            self.on_floor = True
            return
        bottom_rect = pygame.Rect(0, 0, self.rect.width, 2)
        bottom_rect.midtop = self.rect.midbottom
        level_rects = [sprite.rect for sprite in self.collision_sprites]
        self.on_floor = bottom_rect.collidelist(level_rects) >= 0
    
    def animate(self, dt): 
        if not self.frames:
            # Fallback jika aset gambar tidak ada (gambar geometris dinamis)
            self.image = pygame.Surface((32, 48), pygame.SRCALPHA)
            color = (230, 80, 120) if not self.invincible or (pygame.time.get_ticks() // 100) % 2 == 0 else (230, 80, 120, 100)
            pygame.draw.rect(self.image, color, (0, 0, 32, 48), border_radius=4)
            # Eyes
            eye_x = 22 if not self.flip else 6
            pygame.draw.circle(self.image, (255, 255, 255), (eye_x, 15), 4)
            pygame.draw.circle(self.image, (0, 0, 0), (eye_x + (1 if not self.flip else -1), 15), 2)
            return

        if self.animations and isinstance(self.animations, dict):
            # Tentukan state aktif
            if not self.on_floor:
                state = 'jump'
            elif self.dashing:
                state = 'run'
            elif self.direction.x != 0 or (self.movement_mode == "boss" and self.direction.length() > 0):
                state = 'walk' if self.animations.get('walk') else 'run'
            else:
                state = 'idle'
                
            active_frames = self.animations.get(state, [])
            if not active_frames:
                active_frames = self.animations.get('idle', [])
                
            if active_frames:
                # Kecepatan animasi disesuaikan dengan state
                anim_speed = 12 if state in ('run', 'walk') else (6 if state == 'idle' else 10)
                
                # Update frame index
                if state == 'idle' or self.direction.x != 0 or not self.on_floor or self.dashing or (self.movement_mode == "boss" and self.direction.length() > 0):
                    self.frame_index += anim_speed * dt
                else:
                    self.frame_index = 0
                    
                # Dapatkan indeks frame aktif
                if state == 'jump':
                    # Menahan frame di udara pada akhir animasi lompat
                    idx = min(int(self.frame_index), len(active_frames) - 1)
                else:
                    idx = int(self.frame_index) % len(active_frames)
                    
                self.image = active_frames[idx]
                
                # Mengatur hadap (flip)
                if self.movement_mode == "boss":
                    mouse_pos = pygame.mouse.get_pos()
                    player_screen_center = pygame.Vector2(self.rect.center) + self.camera_offset
                    self.flip = mouse_pos[0] < player_screen_center.x
                else:
                    if self.dashing:
                        self.flip = self.dash_direction < 0
                    elif self.direction.x != 0:
                        self.flip = self.direction.x < 0
                        
                self.image = pygame.transform.flip(self.image, self.flip, False)
                return

        # Fallback jika frames berupa list satu dimensi biasa (compat lama)
        if self.movement_mode == "boss":
            # Face the mouse position
            mouse_pos = pygame.mouse.get_pos()
            player_screen_center = pygame.Vector2(self.rect.center) + self.camera_offset
            self.flip = mouse_pos[0] < player_screen_center.x
            
            if self.direction.length() > 0:
                self.frame_index += self.animation_speed * dt 
            else:
                self.frame_index = 0
            self.image = self.frames[int(self.frame_index) % len(self.frames)]
            self.image = pygame.transform.flip(self.image, self.flip, False)
        else:
            if self.dashing:
                self.flip = self.dash_direction < 0
                self.image = pygame.transform.flip(self.frames[1], self.flip, False)
            else:
                if self.direction.x:
                    self.frame_index += self.animation_speed * dt 
                    self.flip = self.direction.x < 0
                else:
                    self.frame_index = 0
                self.frame_index = 1 if not self.on_floor else self.frame_index
                self.image = self.frames[int(self.frame_index) % len(self.frames)]
                self.image = pygame.transform.flip(self.image, self.flip, False)
        
    def update(self, dt):
        self.shoot_timer.update()
        self.dash_timer.update()
        self.dash_cooldown.update()

        # Matikan status dash & kekebalan jika timer dash habis
        if self.dashing and not self.dash_timer:
            self.dashing = False
            self.invincible = False

        self.check_floor()
        self.input()
        self.move(dt)

        # Clamp player position within map boundaries if defined
        map_w = getattr(self, 'map_width', None)
        map_h = getattr(self, 'map_height', None)
        if map_w is not None:
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.right > map_w:
                self.rect.right = map_w
        if map_h is not None:
            if self.rect.top < 0:
                self.rect.top = 0
                self.direction.y = 0
            if self.rect.bottom > map_h:
                self.rect.bottom = map_h
                self.direction.y = 0

        self.animate(dt)

        # Regenerasi Stamina (WP) otomatis jika di bawah max_wp
        if self.wp < self.max_wp:
            self.wp = min(self.max_wp, self.wp + 8 * dt)
            
        # Atur status kelelahan stamina
        if self.wp <= 0:
            self._wp_exhausted = True
        elif self.wp >= 15:
            self._wp_exhausted = False
