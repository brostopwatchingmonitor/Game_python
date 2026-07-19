from settings import *
import pygame

class DefaultCamera:
    def __init__(self):
        self.offset = pygame.Vector2()

    def update(self, target_pos, map_width, map_height):
        self.offset.x = -(target_pos[0] - WINDOW_WIDTH / 2)
        self.offset.y = -(target_pos[1] - WINDOW_HEIGHT / 2)

        if map_width > WINDOW_WIDTH:
            self.offset.x = max(-(map_width - WINDOW_WIDTH), min(0, self.offset.x))
        else:
            self.offset.x = (WINDOW_WIDTH - map_width) / 2

        if map_height > WINDOW_HEIGHT:
            self.offset.y = max(-(map_height - WINDOW_HEIGHT), min(0, self.offset.y))
        else:
            self.offset.y = (WINDOW_HEIGHT - map_height) / 2
        return self.offset

class BossCamera:
    def __init__(self):
        self.offset = pygame.Vector2()

    def update(self, target_pos, map_width, map_height):
        target_x = -(target_pos[0] - WINDOW_WIDTH / 2)
        target_y = -(target_pos[1] - WINDOW_HEIGHT / 2)
        
        self.offset.x += (target_x - self.offset.x) * 0.1
        self.offset.y += (target_y - self.offset.y) * 0.1

        if map_width > WINDOW_WIDTH:
            self.offset.x = max(-(map_width - WINDOW_WIDTH), min(0, self.offset.x))
        else:
            self.offset.x = (WINDOW_WIDTH - map_width) / 2

        if map_height > WINDOW_HEIGHT:
            self.offset.y = max(-(map_height - WINDOW_HEIGHT), min(0, self.offset.y))
        else:
            self.offset.y = (WINDOW_HEIGHT - map_height) / 2
        return self.offset

class CameraManager:
    def __init__(self):
        self.modes = {
            "default": DefaultCamera(),
            "boss": BossCamera()
        }
        self.current_mode = "default"

    def set_mode(self, mode):
        if mode in self.modes:
            self.current_mode = mode

    def update(self, target_pos, map_width, map_height):
        return self.modes[self.current_mode].update(target_pos, map_width, map_height)

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = None
        self.camera_manager = CameraManager()
        self.offset = pygame.Vector2()

    def set_camera_mode(self, mode):
        self.camera_manager.set_mode(mode)

    def draw(self, target_pos, surface=None):
        if surface is not None:
            self.display_surface = surface
        elif self.display_surface is None:
            self.display_surface = pygame.display.get_surface()
            
        map_w = getattr(self, 'map_width', WINDOW_WIDTH)
        map_h = getattr(self, 'map_height', WINDOW_HEIGHT)
        
        self.offset = self.camera_manager.update(target_pos, map_w, map_h)

        for sprite in self:
            draw_offset = getattr(sprite, 'image_offset', pygame.Vector2())
            self.display_surface.blit(sprite.image, sprite.rect.topleft + self.offset + draw_offset)
            
            # Draw Enemy/Boss HP Bar
            if sprite.__class__.__name__ in ('BaseEnemy', 'BossEnemy'):
                bar_w = sprite.rect.width
                bar_h = 6
                ratio = max(0.0, min(1.0, sprite.hp / sprite.max_hp))
                
                screen_x = sprite.rect.left + self.offset.x
                screen_y = sprite.rect.top + self.offset.y - 12
                
                pygame.draw.rect(self.display_surface, (100, 20, 20), (screen_x, screen_y, bar_w, bar_h))
                
                if ratio > 0.5:
                    hp_color = (0, 255, 100)
                elif ratio > 0.2:
                    hp_color = (255, 200, 0)
                else:
                    hp_color = (255, 50, 50)
                    
                if ratio > 0:
                    pygame.draw.rect(self.display_surface, hp_color, (screen_x, screen_y, int(bar_w * ratio), bar_h))
                    
                pygame.draw.rect(self.display_surface, (220, 220, 220), (screen_x, screen_y, bar_w, bar_h), 1)
