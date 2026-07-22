# player.py
import pygame
import os
from settings import *

def import_folder(path):
    surface_list = []
    if os.path.exists(path):
        for _, __, img_files in os.walk(path):
            sorted_files = sorted(img_files, key=lambda x: int(''.join(filter(str.isdigit, x)) or 0))
            for image_name in sorted_files:
                if image_name.endswith('.png'):
                    full_path = os.path.join(path, image_name)
                    try:
                        image_surf = pygame.image.load(full_path).convert_alpha()
                        surface_list.append(image_surf)
                    except Exception as e:
                        print(f"Gagal memuat {image_name}: {e}")
    return surface_list

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites, enemy_sprites=None):
        super().__init__(groups)
        
        # Load Animasi
        self.load_animations()
        self.state = 'idle'
        
        # Variabel Animasi persis seperti Proyek Lama (Tick-Based)
        self.anim_tick = 0
        self.frame_index = 0
        self.anim_speeds = {
            "idle": 20, 
            "run": 8, 
            "jump": 15, 
            "attack_1": 6, 
            "attack_2": 6, 
            "attack_3": 6, 
            "shield": 10
        }
        self.facing_right = True

        # Set gambar awal
        self.image = self.animations['idle'][0] if self.animations['idle'] else pygame.Surface((32, 48))
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox_rect = self.rect.inflate(-12, -4)
        
        # Pergerakan & Fisika
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.hitbox_rect.center)
        self.speed = 200
        self.gravity = 1000
        self.jump_speed = -360
        self.on_floor = False
        
        # Mekanik Double Jump
        self.max_jumps = 2
        self.jump_count = 0
        
        # Mekanik Combat & Shield Combo (Langkah 8 + Combo)
        self.is_attacking = False
        self.is_shielding = False
        self.has_dealt_damage = False
        
        # Sistem Combo
        self.combo_index = 0     
        self.combo_timer = 0     
        self.combo_window = 30   

        # Referensi grup sprite
        self.collision_sprites = collision_sprites
        self.enemy_sprites = enemy_sprites if enemy_sprites is not None else pygame.sprite.Group()

    def load_animations(self):
        self.animations = {
            'idle': [], 'run': [], 'jump': [], 
            'attack_1': [], 'attack_2': [], 'attack_3': [], 
            'shield': []
        }
        
        folder_mapping = {
            'idle': 'idle',
            'run': 'run',
            'jump': 'jump',
            'attack_1': 'attack_1',
            'attack_2': 'attack_2',
            'attack_3': 'attack_3',
            'shield': 'shield'
        }
        
        for state, folder in folder_mapping.items():
            folder_path = os.path.join(ASSETS_DIR, 'image', 'character', folder)
            self.animations[state] = import_folder(folder_path)
            
        for state, frames in self.animations.items():
            if not frames:
                print(f"[Player] Warning: Folder '{state}' kosong. Menggunakan fallback.")
                fallback_surf = pygame.Surface((32, 48))
                fallback_surf.fill((0, 150, 255) if state == 'idle' else (255, 100, 0))
                self.animations[state] = [fallback_surf]

    def input(self):
        if self.is_attacking:
            self.direction.x = 0
            return
            
        keys = pygame.key.get_pressed()
        mouse_buttons = pygame.mouse.get_pressed()
        
        # 1. Mekanik Shield (Klik Kanan Mouse)
        if mouse_buttons[2] and self.on_floor:
            self.is_shielding = True
            self.direction.x = 0
            self.state = "shield"
            self.combo_index = 0
            self.combo_timer = 0
            return
        else:
            self.is_shielding = False
            
        # 2. Mekanik Attack Combo (Klik Kiri Mouse)
        if mouse_buttons[0] and not self.is_attacking:
            if self.combo_timer > 0 and self.combo_timer <= self.combo_window:
                self.combo_index = (self.combo_index % 3) + 1
            else:
                self.combo_index = 1
                
            self.is_attacking = True
            self.has_dealt_damage = False
            self.state = f"attack_{self.combo_index}"
            self.frame_index = 0
            self.anim_tick = 0
            self.direction.x = 0
            self.combo_timer = 0
            return

        # Input horizontal normal
        self.direction.x = 0
        moving = False
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
            self.facing_right = True
            moving = True
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
            self.facing_right = False
            moving = True
            
        # Logika State Gerakan di Tanah
        if self.on_floor:
            if moving:
                self.state = "run"
            else:
                self.state = "idle"

    def jump(self):
        if self.is_attacking or self.is_shielding:
            return
            
        if self.on_floor:
            self.direction.y = self.jump_speed
            self.on_floor = False
            self.combo_index = 0
            self.combo_timer = 0
            self.jump_count = 1
            self.state = "jump"
        elif self.jump_count < self.max_jumps:
            self.direction.y = self.jump_speed
            self.jump_count += 1
            self.state = "jump"

    def update_animation(self):
        self.anim_tick += 1
        speed_threshold = self.anim_speeds.get(self.state, 15)
        
        if self.anim_tick >= speed_threshold:
            self.anim_tick = 0
            self.frame_index += 1
            
        frames = self.animations[self.state]
        
        # Transisi Selesai Menyerang
        if self.state.startswith('attack_') and self.frame_index >= len(frames):
            self.is_attacking = False
            self.state = 'idle'
            self.frame_index = 0
            self.anim_tick = 0
            self.combo_timer = 1 
            frames = self.animations['idle']
            
        # Tahan di frame terakhir jika melompat
        frame_idx = self.frame_index % len(frames)
        if self.state == 'jump' and frame_idx >= len(frames):
            frame_idx = len(frames) - 1
            
        image = frames[frame_idx]
        
        if not self.facing_right:
            self.image = pygame.transform.flip(image, True, False)
        else:
            self.image = image
            
        self.rect = self.image.get_rect(midbottom=self.hitbox_rect.midbottom)

    def check_attack_collisions(self):
        if self.state.startswith('attack_') and not self.has_dealt_damage:
            frames = self.animations[self.state]
            active_frame = len(frames) // 2
            
            if self.frame_index == active_frame:
                hitbox_width = 48
                if self.facing_right:
                    attack_rect = pygame.Rect(self.hitbox_rect.right, self.hitbox_rect.top, hitbox_width, self.hitbox_rect.height)
                    knockback_dir = 1
                else:
                    attack_rect = pygame.Rect(self.hitbox_rect.left - hitbox_width, self.hitbox_rect.top, hitbox_width, self.hitbox_rect.height)
                    knockback_dir = -1
                
                d1 = 20
                d2 = d1 * 2
                d3 = (d1 + d2) * 3
                
                if self.combo_index == 1:
                    damage = d1
                elif self.combo_index == 2:
                    damage = d2
                elif self.combo_index == 3:
                    damage = d3
                else:
                    damage = d1
                    
                for enemy in self.enemy_sprites:
                    if enemy.rect.colliderect(attack_rect):
                        if hasattr(enemy, 'take_damage'):
                            enemy.take_damage(damage, knockback_dir)
                        print(f"[Combo {self.combo_index}] Tebasan mengenai musuh! Damage: {damage}, Arah knockback: {knockback_dir}")
                        self.has_dealt_damage = True

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == 'horizontal':
                    if self.direction.x > 0:
                        self.hitbox_rect.right = sprite.rect.left
                        self.pos.x = self.hitbox_rect.centerx
                    elif self.direction.x < 0:
                        self.hitbox_rect.left = sprite.rect.right
                        self.pos.x = self.hitbox_rect.centerx
                
                elif direction == 'vertical':
                    if self.direction.y > 0:
                        self.hitbox_rect.bottom = sprite.rect.top
                        self.pos.y = self.hitbox_rect.centery
                        self.direction.y = 0
                        self.on_floor = True
                        self.jump_count = 0
                        if self.state == "jump":
                            self.state = "idle"
                    elif self.direction.y < 0:
                        self.hitbox_rect.top = sprite.rect.bottom
                        self.pos.y = self.hitbox_rect.centery
                        self.direction.y = 0

    def move(self, dt):
        # 1. Pergerakan Horizontal
        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox_rect.centerx = round(self.pos.x)
        self.collision('horizontal')
        
        # 2. Pergerakan Vertikal
        if not self.on_floor and self.jump_count == 0:
            self.jump_count = 1
            
        self.on_floor = False
        self.direction.y += self.gravity * dt
        self.pos.y += self.direction.y * dt
        self.hitbox_rect.centery = round(self.pos.y)
        self.collision('vertical')

    def update(self, dt):
        if self.combo_timer > 0:
            self.combo_timer += 1
            if self.combo_timer > self.combo_window:
                self.combo_timer = 0
                self.combo_index = 0
            
        self.input()
        self.move(dt)
        self.update_animation()
        self.check_attack_collisions()
