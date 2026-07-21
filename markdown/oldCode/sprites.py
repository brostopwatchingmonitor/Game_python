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
            # direction is a pygame.Vector2 pointing to the target
            self.direction = direction.normalize()
            # Calculate rotation angle to face target
            angle = math.degrees(math.atan2(-self.direction.y, self.direction.x))
            self.image = pygame.transform.rotate(self.image, angle)
        else:
            # direction is scalar (-1 or 1)
            self.image = pygame.transform.flip(self.image, direction == -1, False)
            self.direction = pygame.Vector2(direction, 0)
        self.speed = 800

    def update(self, dt):
        self.rect.x += self.direction.x * self.speed * dt
        self.rect.y += self.direction.y * self.speed * dt

class AnimatedSprites(Sprites):
    def __init__(self, pos, frames, groups):
        self.frames, self.frame_index, self.animation_speed = frames, 0, 10
        super().__init__(pos, self.frames[self.frame_index], groups)
    def animation(self, dt):
        self.frame_index += self.animation_speed * dt 
        self.image = self.frames[int(self.frame_index) % len(self.frames)]

class Fire(Sprites):
    def __init__(self, surf, pos, groups, player):
        super().__init__(pos, surf, groups)
        self.flip = player.flip
        self.player = player
        self.timer = Timer(100, autostart = True, func = self.kill)
        self.y_offset = pygame.Vector2(0, 8)

        if self.player.flip:
            self.rect.midright = self.player.rect.midleft + self.y_offset
            self.image = pygame.transform.flip(self.image, True, False)
        else:
            self.rect.midleft = self.player.rect.midright + self.y_offset
    def update(self, _):
        self.timer.update()    
        if self.player.flip:
            self.rect.midright = self.player.rect.midleft + self.y_offset
        else:
            self.rect.midleft = self.player.rect.midright + self.y_offset
        if self.flip != self.player.flip:
            self.kill()
