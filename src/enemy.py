# enemy.py
import pygame
import os
import math
import random
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

class BaseEnemy(pygame.sprite.Sprite):
    def __init__(self, pos, enemy_type, groups, collision_sprites, player, game=None):
        super().__init__(groups)
        
        self.enemy_type = enemy_type
        self.player = player
        self.collision_sprites = collision_sprites
        self.game = game # Referensi ke objek Game untuk memicu antrean respawn
        self.spawn_pos = pos
        
        # Load Animasi
        self.load_animations()
        self.state = 'idle'
        self.anim_tick = 0
        self.frame_index = 0
        self.anim_speeds = {"idle": 20, "walk": 10, "attack": 8, "die": 12}
        self.facing_right = False
        
        # Set gambar awal
        self.image = self.animations['idle'][0]
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox_rect = self.rect.inflate(-10, -4)
        
        # Atribut Fisika & Status
        self.direction = pygame.math.Vector2(-1, 0)
        self.pos = pygame.math.Vector2(self.hitbox_rect.center)
        
        # Kecepatan dan atribut sesuai Tier
        is_hard = False
        if self.game is not None and hasattr(self.game, 'player') and self.game.player is not None:
            if self.game.player.level >= 5:
                is_hard = True
                
        if self.enemy_type == 'tier_1':
            self.speed = 100
            self.max_hp = 600 if is_hard else 50
            self.hp = self.max_hp
            self.damage = 10
            self.detection_range = 300
        else: # tier_2
            self.speed = 140
            self.max_hp = 1100 if is_hard else 80
            self.hp = self.max_hp
            self.damage = 15
            self.detection_range = 450
            
        self.gravity = 1000
        self.on_floor = False
        self.is_dead = False
        self.is_attacking = False 
        
        # Hurt Effect Flash (Siluet Putih)
        self.hurt_timer = 0
        self.hurt_duration = 10

    def load_animations(self):
        self.animations = {'idle': [], 'walk': [], 'attack': [], 'die': []}
        base_path = os.path.join(ASSETS_DIR, 'image', 'enemy', 'enemy1')
        
        scale_factor = 1.4
        
        for state in self.animations.keys():
            folder_path = os.path.join(base_path, state)
            frames = import_folder(folder_path)
            
            if state == 'die' and frames:
                frames.reverse()
                
            scaled_frames = []
            for frame in frames:
                w, h = frame.get_size()
                scaled_surf = pygame.transform.scale(frame, (int(w * scale_factor), int(h * scale_factor)))
                scaled_frames.append(scaled_surf)
                
            self.animations[state] = scaled_frames
            
        for state, frames in self.animations.items():
            if not frames:
                fallback_surf = pygame.Surface((44, 67))
                fallback_surf.fill((255, 50, 50) if state == 'attack' else (180, 50, 50))
                self.animations[state] = [fallback_surf]

    def take_damage(self, amount, knockback_dir):
        if self.is_dead:
            return
            
        self.hp -= amount
        self.hurt_timer = self.hurt_duration
        
        self.direction.x = knockback_dir * 1.5
        self.direction.y = -200 * 0.001 * 1000 * 0.1
        self.on_floor = False
        self.is_attacking = False 
        
        if self.hp <= 0:
            self.hp = 0
            self.is_dead = True
            self.state = 'die'
            self.frame_index = 0
            self.anim_tick = 0
            self.direction.x = 0
            
            # Mendaftarkan musuh ini ke antrean respawn di game
            if self.game is not None:
                self.game.queue_respawn(self.spawn_pos, self.enemy_type)

    def patrol_logic_tier1(self):
        if self.is_attacking:
            return
            
        dist_x = self.player.rect.centerx - self.rect.centerx
        dist_y = self.player.rect.centery - self.rect.centery
        distance = math.hypot(dist_x, dist_y)
        
        if distance < self.detection_range:
            if dist_x > 0:
                self.facing_right = True
            else:
                self.facing_right = False
        
        if distance < 80:
            self.is_attacking = True
            self.state = 'attack'
            self.direction.x = 0
            self.frame_index = 0
            self.anim_tick = 0
        elif distance < self.detection_range:
            self.state = 'walk'
            self.direction.x = 1 if dist_x > 0 else -1
        else:
            self.state = 'walk'
            check_offset = 20 if self.facing_right else -20
            check_x = self.hitbox_rect.centerx + check_offset
            check_y = self.hitbox_rect.bottom + 8
            
            has_ground = False
            check_rect = pygame.Rect(check_x - 4, check_y - 4, 8, 8)
            for sprite in self.collision_sprites:
                if sprite.rect.colliderect(check_rect):
                    has_ground = True
                    break
                    
            if self.on_floor and not has_ground:
                self.direction.x *= -1
                self.facing_right = not self.facing_right

    def ai_logic_tier2(self):
        if self.is_attacking:
            return
            
        dist_x = self.player.rect.centerx - self.rect.centerx
        dist_y = self.player.rect.centery - self.rect.centery
        distance = math.hypot(dist_x, dist_y)
        
        if dist_x > 0:
            self.facing_right = True
        else:
            self.facing_right = False
            
        if self.hp < self.max_hp * 0.25:
            self.state = 'walk'
            self.direction.x = -1 if dist_x > 0 else 1
            self.facing_right = self.direction.x > 0
        elif distance < 80:
            self.is_attacking = True
            self.state = 'attack'
            self.direction.x = 0
            self.frame_index = 0
            self.anim_tick = 0
        elif distance < self.detection_range:
            self.state = 'walk'
            self.direction.x = 1 if dist_x > 0 else -1
        else:
            self.state = 'idle'
            self.direction.x = 0

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == 'horizontal':
                    if self.direction.x > 0:
                        self.hitbox_rect.right = sprite.rect.left
                        self.pos.x = self.hitbox_rect.centerx
                        self.direction.x *= -1
                        self.facing_right = not self.facing_right
                    elif self.direction.x < 0:
                        self.hitbox_rect.left = sprite.rect.right
                        self.pos.x = self.hitbox_rect.centerx
                        self.direction.x *= -1
                        self.facing_right = not self.facing_right
                
                elif direction == 'vertical':
                    if self.direction.y > 0:
                        self.hitbox_rect.bottom = sprite.rect.top
                        self.pos.y = self.hitbox_rect.centery
                        self.direction.y = 0
                        self.on_floor = True
                    elif self.direction.y < 0:
                        self.hitbox_rect.top = sprite.rect.bottom
                        self.pos.y = self.hitbox_rect.centery
                        self.direction.y = 0

    def animate(self):
        self.anim_tick += 1
        speed_threshold = self.anim_speeds.get(self.state, 15)
        
        if self.anim_tick >= speed_threshold:
            self.anim_tick = 0
            self.frame_index += 1
            
        frames = self.animations[self.state]
        
        if self.state == 'attack' and self.frame_index >= len(frames):
            self.is_attacking = False
            self.state = 'idle'
            self.frame_index = 0
            self.anim_tick = 0
            frames = self.animations['idle']
            
        if self.state == 'die' and self.frame_index >= len(frames):
            self.kill()
            return
            
        frame_idx = self.frame_index % len(frames)
        image = frames[frame_idx]
        
        if self.facing_right:
            self.image = pygame.transform.flip(image, True, False)
        else:
            self.image = image
            
        if self.hurt_timer > 0:
            self.hurt_timer -= 1
            try:
                mask = pygame.mask.from_surface(self.image)
                silhouette = mask.to_surface(setcolor=(255, 255, 255), unsetcolor=(0, 0, 0, 0))
                self.image = silhouette
            except Exception:
                pass
            
        self.rect = self.image.get_rect(midbottom=self.hitbox_rect.midbottom)

    def move(self, dt):
        if self.is_dead:
            self.direction.y += self.gravity * dt
            self.pos.y += self.direction.y * dt
            self.hitbox_rect.centery = round(self.pos.y)
            self.collision('vertical')
            return
            
        if self.enemy_type == 'tier_1':
            self.patrol_logic_tier1()
        else:
            self.ai_logic_tier2()
            
        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox_rect.centerx = round(self.pos.x)
        self.collision('horizontal')
        
        self.on_floor = False
        self.direction.y += self.gravity * dt
        self.pos.y += self.direction.y * dt
        self.hitbox_rect.centery = round(self.pos.y)
        self.collision('vertical')

    def update(self, dt):
        self.move(dt)
        self.animate()
