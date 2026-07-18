import pygame
import math
from src.setting import (
    COL_RED, COL_WHITE, COL_BLACK, PLAYER_MAX_HP, PLAYER_ATTACK, MOVE_SPEED, XP_BASE
)

class Player:
    def __init__(self, x, y):
        # Posisi & Pergerakan
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.is_grounded = False
        
        # Statistik Player
        self.max_hp = PLAYER_MAX_HP
        self.hp = PLAYER_MAX_HP
        self.gold = 30
        self.xp = 0
        self.atk = PLAYER_ATTACK
        self.speed = MOVE_SPEED
        
        # Timers
        self.invincible_timer = 0.0
        
    def reset(self, x, y):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.hp = self.max_hp
        self.is_grounded = False
        self.invincible_timer = 0.0

    def handle_input(self, keys):
        # Reset kecepatan horizontal
        self.vx = 0
        
        # Input Gerakan Kiri/Kanan
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.vx = -self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.vx = self.speed
            
        # Lompat (Hanya jika menyentuh tanah)
        if (keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]) and self.is_grounded:
            self.vy = -180
            self.is_grounded = False

    def update(self, dt, ground_y, display_width):
        # 1. Update Timer Invincibility
        if self.invincible_timer > 0:
            self.invincible_timer -= dt
            if self.invincible_timer < 0:
                self.invincible_timer = 0
                
        # 2. Terapkan Gravitasi
        self.vy += 500 * dt  # Percepatan gravitasi px/s^2
        if self.vy > 300:     # Batasi kecepatan jatuh maksimal
            self.vy = 300
            
        # 3. Update Posisi
        self.x += self.vx * dt
        self.y += self.vy * dt
        
        # 4. Tabrakan Batas Layar Horizontal
        if self.x < 0:
            self.x = 0
        elif self.x > display_width - 16:
            self.x = display_width - 16
            
        # 5. Tabrakan Tanah (Ground Collision)
        if self.y + 16 >= ground_y:
            self.y = ground_y - 16
            self.vy = 0
            self.is_grounded = True

    def take_damage(self, amount):
        """Mengurangi HP jika sedang tidak invincible. Mengembalikan True jika berhasil terluka."""
        if self.invincible_timer <= 0:
            self.hp -= amount
            if self.hp < 0:
                self.hp = 0
            self.invincible_timer = 1.0  # 1 detik kekebalan setelah terluka
            return True
        return False

    def draw(self, surface):
        # Tampilan berkedip (flickering) jika sedang invincible
        if self.invincible_timer <= 0 or (pygame.time.get_ticks() // 100) % 2 == 0:
            player_rect = pygame.Rect(self.x, self.y, 16, 16)
            pygame.draw.rect(surface, COL_RED, player_rect)
            
            # Mata karakter mengarah sesuai dengan gerakannya
            eye_offset = 11 if self.vx >= 0 else 2
            pygame.draw.rect(surface, COL_WHITE, (self.x + eye_offset, self.y + 3, 3, 3))
            pygame.draw.rect(surface, COL_BLACK, (self.x + eye_offset + (1 if self.vx >= 0 else 0), self.y + 4, 1, 1))
            
    def get_rect(self):
        return pygame.Rect(self.x, self.y, 16, 16)
