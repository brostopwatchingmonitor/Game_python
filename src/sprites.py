# sprites.py
import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox_rect = self.rect.copy()

class DamageText(pygame.sprite.Sprite):
    """Floating Damage, XP, and Status Text effect (ala Final Fantasy)"""
    def __init__(self, pos, val, groups, color=(255, 210, 50)):
        super().__init__(groups)
        
        font = pygame.font.SysFont("Impact", 16)
        
        # Penanganan tipe int (damage) maupun str (Level Up, XP, Blocked)
        if isinstance(val, int):
            text_str = str(val) if val > 0 else "BLOCKED"
        else:
            text_str = str(val)
            
        self.image = font.render(text_str, True, color)
        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.math.Vector2(self.rect.center)
        
        self.speed_y = -60 
        self.lifetime = 0.6 
        self.timer = 0.0

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.lifetime:
            self.kill()
            return
            
        self.pos.y += self.speed_y * dt
        self.rect.centery = round(self.pos.y)
