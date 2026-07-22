# groups.py
import pygame
from settings import *

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.offset = pygame.math.Vector2()
        self.map_width = 0
        self.map_height = 0

    def custom_draw(self, player, display_surface):
        # 1. Hitung offset kamera agar pemain berada di tengah layar
        self.offset.x = player.rect.centerx - RENDER_WIDTH / 2
        self.offset.y = player.rect.centery - RENDER_HEIGHT / 2

        # 2. Batasi (Clamp) kamera agar tidak keluar dari batas Peta
        if self.map_width > RENDER_WIDTH:
            self.offset.x = max(0, min(self.offset.x, self.map_width - RENDER_WIDTH))
        else:
            self.offset.x = 0
            
        if self.map_height > RENDER_HEIGHT:
            self.offset.y = max(0, min(self.offset.y, self.map_height - RENDER_HEIGHT))
        else:
            self.offset.y = -(RENDER_HEIGHT - self.map_height) / 2

        # 3. Gambar semua sprite dikurangi offset kamera
        for sprite in self:
            offset_pos = sprite.rect.topleft - self.offset
            display_surface.blit(sprite.image, offset_pos)

            # 4. Gambar Health Bar di atas kepala Musuh (Langkah 10)
            if hasattr(sprite, 'hp') and hasattr(sprite, 'max_hp') and sprite.__class__.__name__ == 'BaseEnemy':
                # Hanya gambar health bar jika HP di bawah 100% dan musuh masih hidup
                if sprite.hp > 0 and sprite.hp < sprite.max_hp:
                    bar_width = 30
                    bar_height = 4
                    # Posisi di atas kepala musuh dikurangi offset kamera
                    bar_x = sprite.rect.centerx - bar_width / 2 - self.offset.x
                    bar_y = sprite.rect.top - 8 - self.offset.y
                    
                    # Background Bar (Merah)
                    pygame.draw.rect(display_surface, (150, 40, 40), (bar_x, bar_y, bar_width, bar_height))
                    # Foreground Bar (Hijau Terang)
                    hp_ratio = sprite.hp / sprite.max_hp
                    pygame.draw.rect(display_surface, (50, 220, 100), (bar_x, bar_y, int(bar_width * hp_ratio), bar_height))
