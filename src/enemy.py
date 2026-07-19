import pygame
import math
import random
from timer import Timer
from settings import WINDOW_WIDTH, WINDOW_HEIGHT

ENEMY_TYPES = [
    {
        "name"  : "Crab",        # Tier 1 Ground Patrol
        "hp"    : 50,
        "speed" : 108,
        "color" : (220, 80, 60),
        "size"  : (44, 36),
        "damage": 12,
        "xp"    : 35,
        "tier"  : 1,
        "style" : "patrol"
    },
    {
        "name"  : "Jellyfish",   # Tier 1 Flying Hover
        "hp"    : 30,
        "speed" : 144,
        "color" : (100, 180, 255),
        "size"  : (36, 44),
        "damage": 8,
        "xp"    : 20,
        "tier"  : 1,
        "style" : "hover"
    },
    {
        "name"  : "Shark",       # Tier 2 Smart Hunter
        "hp"    : 100,
        "speed" : 150,
        "color" : (160, 160, 200),
        "size"  : (56, 40),
        "damage": 22,
        "xp"    : 75,
        "tier"  : 2,
        "style" : "smart"
    }
]

class BaseEnemy(pygame.sprite.Sprite):
    def __init__(self, pos, name, groups, collision_sprites, player, main_rectangle=None):
        super().__init__(groups)
        self.name = name
        self.player = player
        self.collision_sprites = collision_sprites
        self.main_rectangle = main_rectangle  # Bounding box dari Tiled jika ada

        # Cari konfigurasi tipe musuh
        self.data = next(item for item in ENEMY_TYPES if item["name"] == name)
        
        self.hp = self.data["hp"]
        self.max_hp = self.data["hp"]
        self.speed = self.data["speed"]
        self.damage = self.data["damage"]
        self.color = self.data["color"]
        self.xp = self.data["xp"]
        self.tier = self.data["tier"]
        self.style = self.data["style"]
        
        self.width, self.height = self.data["size"]
        self.image = self._make_surface()
        self.rect = self.image.get_rect(topleft = pos)
        
        # State AI
        self.direction = pygame.Vector2(-1, 0)
        self.vy = 0.0
        self.gravity = 30.0
        
        # Properti Kematian (Silhouette Death Effect)
        self.dying = False
        self.death_timer = None

        # Properti Gerakan Melayang Gelombang Sinus (Tier 1 Hover)
        self.amplitude = random.randint(300, 500)
        self.frequency = random.randint(200, 400)
        
        # Properti AI Pintar (Tier 2 Smart)
        self.ai_state = "patrol"  # patrol, chase, searching, flee
        self.aggro_range = 350
        self.shoot_range = 250
        self.last_known_player_pos = None
        
        self.search_timer = None
        self.shoot_cooldown = Timer(1500)  # Tembak setiap 1.5 detik
        
        self.flip = False
        self.mask = pygame.mask.from_surface(self.image)

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
        if self.dying:
            return
        self.hp -= amount
        if self.hp <= 0:
            self.hp = 0
            self.dying = True
            self.speed = 0
            
            # Efek Siluet Putih (Silhouette Death Effect)
            self.image = self._make_surface()
            if self.flip:
                self.image = pygame.transform.flip(self.image, True, False)
            mask = pygame.mask.from_surface(self.image)
            self.image = mask.to_surface(setcolor=(255, 255, 255), unsetcolor=(0, 0, 0))
            self.image.set_colorkey((0, 0, 0))
            
            # Timer Kematian 200ms (Pembersihan Objek memori)
            self.death_timer = Timer(200, autostart=True, func=self.kill)

    def update(self, dt):
        if self.dying:
            if self.death_timer:
                self.death_timer.update()
            return

        # Ambil jarak pemain
        dist_x = self.player.rect.centerx - self.rect.centerx
        dist_y = self.player.rect.centery - self.rect.centery
        dist = math.hypot(dist_x, dist_y)

        # ── KEPUTUSAN AI ──
        if self.tier == 1:
            self.update_tier1(dt)
        else:
            self.update_tier2(dt, dist, dist_x, dist_y)

        # Bergerak & Tabrakan
        if self.style == "hover" or (self.tier == 2 and self.ai_state != "patrol"):
            # Gerakan terbang/renang dinamis
            self.rect.x += self.direction.x * self.speed * dt
            self.collision('horizontal')
            self.rect.y += self.direction.y * self.speed * dt
            self.collision('vertical')
        else:
            # Gerakan berbasis gravitasi (darat)
            self.rect.x += self.direction.x * self.speed * dt
            self.collision('horizontal')
            
            self.vy += self.gravity * dt
            self.rect.y += self.vy
            self.collision('vertical')

        # Redraw dan arah hadap
        self.flip = self.direction.x > 0
        self.image = self._make_surface()
        if self.flip:
            self.image = pygame.transform.flip(self.image, True, False)
            
        self.mask = pygame.mask.from_surface(self.image)

    # ── TIER 1: PATROL & HOVER LOGIC ──
    def update_tier1(self, dt):
        if self.style == "patrol":
            # Jika di luar batas Tiled rectangle patroli, balik arah
            if self.main_rectangle and not self.main_rectangle.contains(self.rect):
                self.direction.x *= -1
                self.rect.x += self.direction.x * 5
                
            # Jika tidak ada area batasan, gunakan cek jurang/tabrakan dinding
            elif not self.main_rectangle:
                # Cek sensor depan bawah (apakah ada lantai)
                sensor_x = self.rect.right + 10 if self.direction.x > 0 else self.rect.left - 10
                sensor_y = self.rect.bottom + 5
                has_floor = False
                for block in self.collision_sprites:
                    if block.rect.collidepoint(sensor_x, sensor_y):
                        has_floor = True
                        break
                if not has_floor:
                    self.direction.x *= -1
                    
        elif self.style == "hover":
            # Osilasi vertikal gelombang sinus
            self.vy = math.sin(pygame.time.get_ticks() / self.frequency) * self.amplitude * dt
            self.direction.y = self.vy / 10.0 if self.vy != 0 else 0

    # ── TIER 2: SMART AI STATE MACHINE ──
    def update_tier2(self, dt, dist, dist_x, dist_y):
        self.shoot_cooldown.update()
        if self.search_timer:
            self.search_timer.update()

        # State Flee (HP < 25%)
        if self.hp < (self.max_hp * 0.25):
            self.ai_state = "flee"
            # Lari menjauh dari arah player
            self.direction.x = -1 if dist_x > 0 else 1
            
            # Ahead-sensor untuk mendeteksi dinding/tebing saat kabur agar tidak tersangkut
            sensor_x = self.rect.centerx + (self.direction.x * 32)
            sensor_y = self.rect.bottom + 10
            
            hit_wall = False
            for block in self.collision_sprites:
                if block.rect.collidepoint(sensor_x, self.rect.centery):
                    hit_wall = True
                    break
            
            # Jika di depan ada dinding, AI lompat/menghindar atau berbalik arah bertahan
            if hit_wall:
                self.direction.y = -10  # Mencoba lompat menghindari tebing
                
        # State Chase
        elif dist < self.aggro_range:
            self.ai_state = "chase"
            self.last_known_player_pos = pygame.Vector2(self.player.rect.center)
            
            # Bergerak mendekati player
            self.direction.x = 1 if dist_x > 0 else -1
            if abs(dist_y) > 20:
                self.direction.y = 1 if dist_y > 0 else -1
            else:
                self.direction.y = 0
                
            # Logika Menyerang Jarak Jauh (Ranged Attack)
            if dist < self.shoot_range and not self.shoot_cooldown:
                self.direction.x = 0  # Berhenti sejenak untuk membidik
                self.shoot_projectile(dist_x, dist_y)
                self.shoot_cooldown.activate()
                
        # State Searching (Jika player keluar Aggro Range)
        elif self.ai_state == "chase":
            self.ai_state = "searching"
            
            def back_to_patrol():
                self.ai_state = "patrol"
                self.direction.x = -1 if random.random() < 0.5 else 1
                self.direction.y = 0
                
            # Mulai Cooldown Memori Selama 3 Detik
            self.search_timer = Timer(3000, autostart=True, func=back_to_patrol)
            
        elif self.ai_state == "searching":
            # Berjalan mendekati posisi terakhir player diingat
            if self.last_known_player_pos:
                last_dist_x = self.last_known_player_pos.x - self.rect.centerx
                if abs(last_dist_x) > 10:
                    self.direction.x = 1 if last_dist_x > 0 else -1
                else:
                    self.last_known_player_pos = None

        # State Patrol Default
        else:
            self.ai_state = "patrol"
            self.direction.y = 0

    def shoot_projectile(self, dx, dy):
        # Tembak peluru musuh ke arah koordinat player
        from sprites import Bullet
        bullet_surf = pygame.Surface((12, 12), pygame.SRCALPHA)
        pygame.draw.circle(bullet_surf, (255, 60, 60), (6, 6), 6) # Peluru merah musuh
        
        dir_vec = pygame.Vector2(dx, dy)
        if dir_vec.length() > 0:
            dir_vec = dir_vec.normalize()
        else:
            dir_vec = pygame.Vector2(-1, 0)
            
        Bullet(bullet_surf, self.rect.center, dir_vec, (self.groups()[0], self.player.collision_sprites), mode="boss")

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if direction == 'horizontal':
                    if self.direction.x > 0:
                        self.rect.right = sprite.rect.left
                        if self.ai_state == "patrol": self.direction.x *= -1
                    elif self.direction.x < 0:
                        self.rect.left = sprite.rect.right
                        if self.ai_state == "patrol": self.direction.x *= -1
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
        self.stage_idx = 2
        
        self.width, self.height = 96, 96
        self.image = self._make_surface()
        self.rect = self.image.get_rect(center = pos)
        
        self.direction = pygame.Vector2()
        self.shoot_timer = Timer(1200, autostart=True)
        self.bullet_surf = pygame.Surface((18, 18), pygame.SRCALPHA)
        pygame.draw.circle(self.bullet_surf, (255, 60, 60), (9, 9), 9)

        self.ai_state = "idle"
        self.action_timer = Timer(2000, autostart=True)
        self.bullets_fired = 0
        self.dying = False
        self.death_timer = None
        self.mask = pygame.mask.from_surface(self.image)

    def _make_surface(self):
        w, h = self.width, self.height
        surf = pygame.Surface((w, h), pygame.SRCALPHA)
        
        pygame.draw.ellipse(surf, self.color, (12, 12, w-24, h-24))
        pygame.draw.ellipse(surf, (0, 0, 0), (w//4, h//3, w//2, h//3))
        
        eye_color = (0, 255, 200) if self.phase == 1 else ((255, 150, 0) if self.phase == 2 else (255, 0, 80))
        pygame.draw.circle(surf, eye_color, (w//2, h//2), 12)
        pygame.draw.circle(surf, (255, 255, 255), (w//2 - 3, h//2 - 3), 3)
        
        for i in range(8):
            angle = i * (math.pi / 4)
            x1 = w//2 + int(math.cos(angle) * (w//2 - 12))
            y1 = h//2 + int(math.sin(angle) * (h//2 - 12))
            x2 = w//2 + int(math.cos(angle) * (w//2))
            y2 = h//2 + int(math.sin(angle) * (h//2))
            pygame.draw.line(surf, (150, 0, 180), (x1, y1), (x2, y2), 4)

        return surf

    def take_damage(self, amount):
        if self.dying:
            return
        self.hp -= amount
        if self.hp <= 0:
            self.hp = 0
            self.dying = True
            self.speed = 0
            
            # Efek Siluet Putih (Silhouette Death Effect)
            self.image = self._make_surface()
            mask = pygame.mask.from_surface(self.image)
            self.image = mask.to_surface(setcolor=(255, 255, 255), unsetcolor=(0, 0, 0))
            self.image.set_colorkey((0, 0, 0))
            self.death_timer = Timer(200, autostart=True, func=self.kill)
            return
            
        if self.hp > 800:
            self.phase = 1
        elif 400 < self.hp <= 800:
            if self.phase == 1:
                self.phase = 2
                self.speed = 180
                self.shoot_timer.duration = 800
        else:
            if self.phase == 2:
                self.phase = 3
                self.speed = 240
                self.shoot_timer.duration = 400

    def update(self, dt):
        if self.dying:
            if self.death_timer:
                self.death_timer.update()
            return

        self.shoot_timer.update()
        self.action_timer.update()
        
        dist_x = self.player.rect.centerx - self.rect.centerx
        dist_y = self.player.rect.centery - self.rect.centery
        dist = math.hypot(dist_x, dist_y)
        
        if not self.action_timer:
            states = ["charge", "orbit", "shoot"]
            self.ai_state = random.choice(states)
            self.action_timer = Timer(random.randint(1500, 3000), autostart=True)
            self.bullets_fired = 0
            
        if self.ai_state == "charge":
            if dist > 0:
                self.direction = pygame.Vector2(dist_x, dist_y).normalize()
            else:
                self.direction = pygame.Vector2()
        elif self.ai_state == "orbit":
            if dist > 0:
                dir_to_player = pygame.Vector2(dist_x, dist_y).normalize()
                self.direction = pygame.Vector2(-dir_to_player.y, dir_to_player.x)
            else:
                self.direction = pygame.Vector2()
        else:
            self.direction = pygame.Vector2()
            
        if not self.shoot_timer and dist < 600:
            dir_to_player = pygame.Vector2(dist_x, dist_y)
            if dir_to_player.length() > 0:
                from sprites import Bullet
                Bullet(self.bullet_surf, self.rect.center, dir_to_player, self.groups(), mode="boss")
            self.shoot_timer.activate()
            
        self.rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')
        self.rect.y += self.direction.y * self.speed * dt
        self.collision('vertical')
        
        self.image = self._make_surface()
        self.mask = pygame.mask.from_surface(self.image)

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if direction == 'horizontal':
                    if self.direction.x > 0:
                        self.rect.right = sprite.rect.left
                    elif self.direction.x < 0:
                        self.rect.left = sprite.rect.right
                elif direction == 'vertical':
                    if self.direction.y > 0:
                        self.rect.bottom = sprite.rect.top
                    elif self.direction.y < 0:
                        self.rect.top = sprite.rect.bottom
