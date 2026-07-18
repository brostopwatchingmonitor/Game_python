import pygame
from src.setting import COL_WHITE, COL_BLACK, COL_GOLD, COL_DARK_GRAY, COL_ACCENT

# Inisialisasi Font Pygame secara global
pygame.font.init()

def get_font(size):
    # Menggunakan font bawaan pygame (None) yang terlihat sangat retro pada resolusi rendah (400x300)
    return pygame.font.Font(None, size)

def draw_text(surface, text, x, y, size=16, color=COL_WHITE, center=False):
    font = get_font(size)
    text_surface = font.render(text, False, color)  # False untuk antialiasing agar pixel art tajam
    text_rect = text_surface.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    surface.blit(text_surface, text_rect)

class RetroPanel:
    """Panel bergaya retro dengan border ganda dan bayangan pixel."""
    def __init__(self, x, y, width, height, bg_color=COL_DARK_GRAY, border_color=COL_WHITE):
        self.rect = pygame.Rect(x, y, width, height)
        self.bg_color = bg_color
        self.border_color = border_color
        
    def draw(self, surface):
        # 1. Gambar bayangan hitam (offset 2 pixel ke kanan bawah)
        shadow_rect = self.rect.copy()
        shadow_rect.x += 2
        shadow_rect.y += 2
        pygame.draw.rect(surface, COL_BLACK, shadow_rect)
        
        # 2. Gambar background panel utama
        pygame.draw.rect(surface, self.bg_color, self.rect)
        
        # 3. Gambar border luar (putih)
        pygame.draw.rect(surface, self.border_color, self.rect, 1)
        
        # 4. Gambar border dalam (jarak 2px dari border luar)
        inner_rect = pygame.Rect(self.rect.x + 2, self.rect.y + 2, self.rect.width - 4, self.rect.height - 4)
        pygame.draw.rect(surface, self.border_color, inner_rect, 1)

class RetroButton:
    """Tombol interaktif dengan deteksi hover mouse atau pilihan keyboard."""
    def __init__(self, x, y, width, height, text, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.is_hovered = False
        
    def check_hover(self, mouse_pos):
        # Posisi mouse perlu disesuaikan dengan skala screen (diatur di game loop)
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        return self.is_hovered
        
    def draw(self, surface, is_selected=False):
        # Tombol aktif jika mouse hover ATAU jika dipilih lewat keyboard (is_selected)
        active = self.is_hovered or is_selected
        
        # Background dan Border
        bg_col = COL_DARK_GRAY if not active else COL_ACCENT
        border_col = COL_WHITE if not active else COL_GOLD
        text_col = COL_WHITE if not active else COL_BLACK
        
        # Panel tombol
        panel = RetroPanel(self.rect.x, self.rect.y, self.rect.width, self.rect.height, bg_color=bg_col, border_color=border_col)
        panel.draw(surface)
        
        # Tulisan tombol di tengah
        draw_text(surface, self.text, self.rect.centerx, self.rect.centery, size=16, color=text_col, center=True)

class ProgressBar:
    """Bar status untuk HP, Mana, XP, dll. dengan border luar."""
    def __init__(self, x, y, width, height, current_val, max_val, bar_color, bg_color=COL_DARK_GRAY):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.current_val = current_val
        self.max_val = max_val
        self.bar_color = bar_color
        self.bg_color = bg_color
        
    def draw(self, surface, current_val):
        self.current_val = max(0, min(current_val, self.max_val))
        
        # Background bar
        bg_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(surface, self.bg_color, bg_rect)
        
        # Isi bar (proporsional)
        fill_width = int((self.current_val / self.max_val) * (self.width - 4))
        if fill_width > 0:
            fill_rect = pygame.Rect(self.x + 2, self.y + 2, fill_width, self.height - 4)
            pygame.draw.rect(surface, self.bar_color, fill_rect)
            
        # Border terluar
        pygame.draw.rect(surface, COL_WHITE, bg_rect, 1)

class DialogueBox:
    """Dialog Box dengan efek typewriter berjalan per karakter."""
    def __init__(self, x, y, width, height):
        self.panel = RetroPanel(x, y, width, height)
        self.text_list = []
        self.current_line_idx = 0
        self.displayed_text = ""
        self.char_idx = 0
        self.speed = 1.0  # Kecepatan penambahan huruf per frame (1 huruf/frame)
        self.timer = 0
        self.speaker_name = "NPC"
        
    def start_dialogue(self, speaker, lines):
        self.speaker_name = speaker
        self.text_list = lines
        self.current_line_idx = 0
        self.displayed_text = ""
        self.char_idx = 0
        self.timer = 0
        
    def update(self):
        if self.current_line_idx < len(self.text_list):
            target_text = self.text_list[self.current_line_idx]
            if self.char_idx < len(target_text):
                self.timer += 1
                if self.timer >= 2:  # Tambahkan 1 karakter setiap 2 frame
                    self.char_idx += 1
                    self.displayed_text = target_text[:self.char_idx]
                    self.timer = 0
            
    def next_line(self):
        """Lanjut ke dialog berikutnya. Return True jika masih ada dialog, False jika selesai."""
        if self.current_line_idx < len(self.text_list):
            target_text = self.text_list[self.current_line_idx]
            # Jika teks belum selesai diketik, selesaikan instan
            if self.char_idx < len(target_text):
                self.char_idx = len(target_text)
                self.displayed_text = target_text
                return True
            else:
                # Jika sudah selesai diketik, lanjut baris baru
                self.current_line_idx += 1
                self.char_idx = 0
                self.displayed_text = ""
                if self.current_line_idx < len(self.text_list):
                    return True
        return False

    def draw(self, surface):
        # Gambar kotak panel
        self.panel.draw(surface)
        
        # Nama Pembicara
        name_y = self.panel.rect.y + 8
        draw_text(surface, f"[{self.speaker_name}]", self.panel.rect.x + 10, name_y, size=14, color=COL_GOLD)
        
        # Isi Percakapan (bungkus kata sederhana jika melebihi lebar panel)
        words = self.displayed_text.split(' ')
        lines_to_draw = []
        current_line = ""
        max_width = self.panel.rect.width - 24
        
        for word in words:
            # Uji ukuran teks jika ditambahkan kata baru
            test_line = current_line + " " + word if current_line else word
            font = get_font(12)
            if font.size(test_line)[0] < max_width:
                current_line = test_line
            else:
                lines_to_draw.append(current_line)
                current_line = word
        if current_line:
            lines_to_draw.append(current_line)
            
        # Gambar baris teks dialog
        start_y = name_y + 16
        for i, line in enumerate(lines_to_draw[:3]):  # Batasi maks 3 baris
            draw_text(surface, line, self.panel.rect.x + 12, start_y + (i * 12), size=12, color=COL_WHITE)
            
        # Tanda panah petunjuk "Lanjut" (berkedip)
        if self.current_line_idx < len(self.text_list):
            target_text = self.text_list[self.current_line_idx]
            if self.char_idx >= len(target_text):  # Muncul hanya jika text baris ini selesai diketik
                if (pygame.time.get_ticks() // 400) % 2 == 0:
                    draw_text(surface, "V", self.panel.rect.right - 15, self.panel.rect.bottom - 15, size=12, color=COL_ACCENT)
