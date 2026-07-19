from settings import *
from timer import Timer
import math

class Sprites(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)

class Bullet(Sprites):
    def __init__(self, surf, pos, direction, groups, mode="default"):
        super().__init__(pos, surf, groups)
        self.mode = mode
        if self.mode == "boss":
            self.direction = direction.normalize()
            angle = math.degrees(math.atan2(-self.direction.y, self.direction.x))
            self.image = pygame.transform.rotate(self.image, angle)
        else:
            self.image = pygame.transform.flip(self.image, direction == -1, False)
            self.direction = pygame.Vector2(direction, 0)
        self.speed = 800

    def update(self, dt):
        self.rect.x += self.direction.x * self.speed * dt
        self.rect.y += self.direction.y * self.speed * dt

class AnimatedSprites(Sprites):
    def __init__(self, pos, frames, groups):
        self.frames = frames
        self.frame_index = 0
        self.animation_speed = 10
        if not self.frames:
            # Fallback surface jika list frame kosong
            surf = pygame.Surface((32, 48), pygame.SRCALPHA)
            super().__init__(pos, surf, groups)
        else:
            super().__init__(pos, self.frames[self.frame_index], groups)
            
    def animation(self, dt):
        if self.frames:
            self.frame_index += self.animation_speed * dt 
            self.image = self.frames[int(self.frame_index) % len(self.frames)]

class VisualEffect(Sprites):
    """Efek visual generik seperti hit spark, muzzle flash, tebasan pedang, dll.
    Mendukung penjangkaran ke objek bergerak (target_anchor), orientasi hadap,
    dan sinkronisasi trigger suara SFX saat efek dimulai. Melakukan garbage
    collection otomatis (self.kill) saat durasi habis.
    """
    def __init__(self, pos, surf, groups, duration=150, target_anchor=None, offset=None, flip=False, sound=None):
        super().__init__(pos, surf, groups)
        self.duration = duration
        self.target_anchor = target_anchor
        self.offset = offset if offset is not None else pygame.Vector2()
        self.flip = flip
        
        if self.flip:
            self.image = pygame.transform.flip(self.image, True, False)
            
        if self.target_anchor:
            self.update_position()
            
        # Garbage collection timer
        self.timer = Timer(self.duration, autostart=True, func=self.kill)
        
        # Sinkronisasi Trigger Suara SFX
        if sound:
            try:
                sound.play()
            except Exception as e:
                print(f"[VisualEffect] Gagal memutar suara: {e}")

    def update_position(self):
        if self.target_anchor:
            self.rect.center = pygame.Vector2(self.target_anchor.rect.center) + self.offset

    def update(self, dt):
        self.timer.update()
        if self.target_anchor:
            self.update_position()
            # Jika objek target mati, hapus efek
            if not self.target_anchor.alive():
                self.kill()
