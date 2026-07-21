import pygame
import math
import random
from timer import Timer
from settings import WINDOW_WIDTH, WINDOW_HEIGHT

# Data tipe musuh dari Project 1 settings
ENEMY_TYPES = [
    {
        "name"  : "Crab",
        "hp"    : 50,
        "speed" : 108, # 1.8 * 60 (disesuaikan untuk delta time)
        "color" : (220, 80, 60),
        "size"  : (44, 36),
        "damage": 12,
        "xp"    : 35,
    },
    {
        "name"  : "Jellyfish",
        "hp"    : 30,
        "speed" : 144, # 2.4 * 60
        "color" : (100, 180, 255),
        "size"  : (36, 44),
        "damage": 8,
        "floats": True,
        "xp"    : 20,
    },
    {
        "name"  : "Shark",
        "hp"    : 80,
        "speed" : 168, # 2.8 * 60
        "color" : (160, 160, 200),
        "size"  : (56, 40),
        "damage": 20,
        "xp"    : 50,
    }
]

class BaseEnemy(pygame.sprite.Sprite):
    def __init__(self, pos, name, groups, collision_sprites, player):
        super().__init__(groups)
        self.name = name
        self.player = player
        self.collision_sprites = collision_sprites

        # Cari data musuh
        self.data = next(item for item in ENEMY_TYPES if item["name"] == name)
        
        self.hp = self.data["hp"]
        self.max_hp = self.data["hp"]
        self.speed = self.data["speed"]
        self.damage = self.data["damage"]
        self.color = self.data["color"]
        self.floats = self.data.get("floats", False)
        self.xp = self.data.get("xp", 10)
        
        self.width, self.height = self.data["size"]
        self.image = self._make_surface()
        self.rect = self.image.get_rect(topleft = pos)
        
        # State AI & Pergerakan
        self.direction = pygame.Vector2(-1, 0)
        self.vy = 0.0
        self.gravity = 30.0
        
        self._aggro = False
        self._aggro_range = 300
        self._bob = 0.0
        self._bob_dir = 1
        self.flip = False

    def _make_surface(self):
        w, h = self.width, self.height
        surf = pygame.Surface((w, h), pygame.SRCALPHA)

        if self.name == "Crab":
            pygame.draw.ellipse(surf, self.color, (4, h//3, w-8, h*2//3))
            pygame.draw.polygon(surf, (min(255, self.color[0]+20), self.color[1], self.color[2]), [
                (0, h//2), (8, h//3), (0, h//4)
            ])
            pygame.draw.polygon(surf, (min(255, self.color[0]+20), self.color[1], self.color[2]), [
                (w, h//2), (w-8, h//3), (w, h//4)
            ])
            pygame.draw.circle(surf, (0,0,0), (w//3, h//3+2), 3)
            pygame.draw.circle(surf, (0,0,0), (2*w//3, h//3+2), 3)
            for i in range(3):
                leg_x = 6 + i*10
                pygame.draw.line(surf, self.color, (leg_x, h-4), (leg_x-4, h), 2)
                pygame.draw.line(surf, self.color, (w-6-i*10, h-4), (w-2-i*10, h), 2)

        elif self.name == "Jellyfish":
            pygame.draw.ellipse(surf, (*self.color, 180), (2, 2, w-4, h//2))
            pygame.draw.ellipse(surf, (*self.color[:3], 60), (0, 0, w, h//2+4))
            for i in range(5):
                tx = 4 + i * (w-8)//4
                for j in range(3):
                    ty = h//2 + j*6
                    pygame.draw.circle(surf, (*self.color[:3], 140), (tx, ty), 2)
            pygame.draw.ellipse(surf, (200, 240, 255, 200), (w//4, h//8, w//2, h//4))

        elif self.name == "Shark":
            pygame.draw.ellipse(surf, self.color, (0, h//4, w, h//2))
            pygame.draw.polygon(surf, (max(0, self.color[0]-20), max(0, self.color[1]-20), min(255, self.color[2]+20)), [
                (w//2, h//4), (w//2+15, 0), (w//2+20, h//4)
            ])
            pygame.draw.polygon(surf, self.color, [
                (w-4, h//2-5), (w+8, h//4), (w+8, 3*h//4), (w-4, h//2+5)
            ])
            pygame.draw.circle(surf, (10,10,10), (12, h//2-2), 4)
            pygame.draw.circle(surf, (255,255,255), (11, h//2-3), 1)
            pygame.draw.arc(surf, (255,255,255), (4, h//2, 16, 8), 0, math.pi, 2)

        return surf

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.kill()

    def update(self, dt):
        dist_x = self.player.rect.centerx - self.rect.centerx
        dist_y = self.player.rect.centery - self.rect.centery
        dist = math.hypot(dist_x, dist_y)

        if dist < self._aggro_range:
            self._aggro = True

        if self._aggro:
            if dist_x > 0:
                self.direction.x = 1
            else:
                self.direction.x = -1
        else:
            self.direction.x = -0.6

        self.flip = self.direction.x > 0

        # Movement
        self.rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')

        if self.floats:
            self._bob += 5 * dt * self._bob_dir
            if abs(self._bob) > 8:
                self._bob_dir *= -1
            target_y = self.player.rect.centery + random.randint(-60, 60) if self._aggro else WINDOW_HEIGHT // 2
            diff_y = target_y - self.rect.centery
            self.vy = max(-120, min(120, diff_y * 1.8))
            self.rect.y += self.vy * dt
        else:
            self.vy += self.gravity * dt
            self.rect.y += self.vy
            self.collision('vertical')

        self.image = self._make_surface()
        if self.flip:
            self.image = pygame.transform.flip(self.image, True, False)

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if direction == 'horizontal':
                    if self.direction.x > 0:
                        self.rect.right = sprite.rect.left
                    elif self.direction.x < 0:
                        self.rect.left = sprite.rect.right
                elif direction == 'vertical':
                    if self.vy > 0:
                        self.rect.bottom = sprite.rect.top
                        self.vy = 0
                    elif self.vy < 0:
                        self.rect.top = sprite.rect.bottom
                        self.vy = 0


class BossEnemy(pygame.sprite.Sprite):
    def __init__(self, pos, name, groups, collision_sprites, player):
        super().__init__(groups)
        self.name = name
        self.player = player
        self.collision_sprites = collision_sprites
        
        self.hp = 1200
        self.max_hp = 1200
        self.speed = 120
        self.damage = 35
        self.color = (200, 0, 255)
        self.xp = 1000
        self.phase = 1
        self.stage_idx = 2  # Stage 3 is index 2
        
        self.width, self.height = 96, 96
        self.image = self._make_surface()
        self.rect = self.image.get_rect(center = pos)
        
        self.direction = pygame.Vector2()
        self.shoot_timer = Timer(1200, autostart=True)
        self.bullet_surf = pygame.Surface((18, 18), pygame.SRCALPHA)
        pygame.draw.circle(self.bullet_surf, (255, 60, 60), (9, 9), 9)

    def _make_surface(self):
        surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.circle(surf, (15, 0, 30), (self.width//2, self.height//2), self.width//2)
        pygame.draw.circle(surf, self.color, (self.width//2, self.height//2), self.width//2 - 4, 4)
        pygame.draw.circle(surf, (255, 0, 80), (self.width//2, self.height//2), 18)
        pygame.draw.circle(surf, (255, 255, 255), (self.width//2, self.height//2), 32, 2)
        return surf

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 800 and self.phase == 1:
            self.phase = 2
            self.speed = 180
            self.shoot_timer.duration = 800
            print("Boss Phase 2!")
        elif self.hp <= 400 and self.phase == 2:
            self.phase = 3
            self.speed = 260
            self.shoot_timer.duration = 400
            print("Boss Phase 3!")

        if self.hp <= 0:
            self.kill()

    def update(self, dt):
        self.shoot_timer.update()
        
        player_pos = pygame.Vector2(self.player.rect.center)
        boss_pos = pygame.Vector2(self.rect.center)
        self.direction = (player_pos - boss_pos)
        if self.direction.length() > 0:
            self.direction = self.direction.normalize()
            
        self.rect.x += self.direction.x * self.speed * dt
        self.rect.y += self.direction.y * self.speed * dt

        # Spawn boss bullets
        if not self.shoot_timer:
            self.shoot_timer.activate()
            groups = self.groups()
            
            dir_to_player = (player_pos - boss_pos)
            if dir_to_player.length() > 0:
                dir_to_player = dir_to_player.normalize()
            
            from sprites import Bullet
            Bullet(self.bullet_surf, self.rect.center, dir_to_player, groups, mode="boss")
            
            if self.phase >= 2:
                for angle in [45, -45]:
                    rotated_dir = dir_to_player.rotate(angle)
                    Bullet(self.bullet_surf, self.rect.center, rotated_dir, groups, mode="boss")
            if self.phase == 3:
                for angle in [90, -90, 180]:
                    rotated_dir = dir_to_player.rotate(angle)
                    Bullet(self.bullet_surf, self.rect.center, rotated_dir, groups, mode="boss")
