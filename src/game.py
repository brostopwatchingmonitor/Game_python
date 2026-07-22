# game.py
import pygame
import sys
from settings import *

class Game:
    def __init__(self):
        pygame.init()
        # Window utama (screen fisik)
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("2D Platformer - Step 1")
        
        # Canvas internal untuk rendering pixel art (resolusi lebih rendah untuk efek pixelated)
        self.display_surface = pygame.Surface((RENDER_WIDTH, RENDER_HEIGHT))
        
        self.clock = pygame.time.Clock()
        self.running = True
        
        # State Machine Dasar
        self.state = STATE_PLAYING

    def run(self):
        while self.running:
            # 1. Kalkulasi Delta Time (dt)
            # tick(FPS) mengembalikan milliseconds sejak frame terakhir. Dibagi 1000.0 untuk mendapatkan detik.
            dt = self.clock.tick(FPS) / 1000.0
            
            # Batasi dt maksimum agar tidak melompat terlalu jauh jika lag terjadi
            if dt > 0.1:
                dt = 0.1

            # 2. Event Loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

            # 3. Game Logic & Rendering berdasarkan State
            if self.state == STATE_PLAYING:
                # Update logic (untuk Langkah 1, kita hanya membersihkan layar terlebih dahulu)
                self.display_surface.fill((30, 30, 40)) # Background warna abu-abu kebiruan gelap
                
                # Menggambar objek dummy sebagai penanda canvas berfungsi
                pygame.draw.rect(self.display_surface, (0, 255, 150), (100, 100, 50, 50))

            # 4. Scaling dan Rendering ke Layar Utama
            # Lakukan upscale dari display_surface (resolusi internal) ke screen fisik
            scaled_surface = pygame.transform.scale(self.display_surface, (WINDOW_WIDTH, WINDOW_HEIGHT))
            self.screen.blit(scaled_surface, (0, 0))
            
            pygame.display.flip()

        pygame.quit()
        sys.exit()
