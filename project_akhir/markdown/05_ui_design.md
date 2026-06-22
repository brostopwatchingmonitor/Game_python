# Rancangan 5: Desain UI (Pygame Screens)

Karena Pygame adalah *engine* berbasis *Surface* (kanvas gambar), kita tidak bisa menggunakan tag HTML atau *widget* bawaan. Setiap elemen UI harus digambar manual piksel demi piksel di dalam *game loop*.

## Alur Layar (Screen Flow)

1. **Splash Screen** (Opsional - 2 detik) -> Transisi ke Menu.
2. **Main Menu Screen** -> Input Nama Pemain, Tombol "Main", "Leaderboard", "Keluar".
3. **Play Screen** -> *Core gameplay* (menampilkan soal, UI timer bar, UI sisa nyawa).
4. **Game Over Screen** -> Menampilkan hasil skor, kalkulasi animasi, dan tombol kembali ke Menu.

## Komponen Kustom UI Pygame

Untuk menghindari duplikasi kode saat membuat tombol "Mulai" dan "Keluar", buat kelas *Button* yang dinamis.

```python
# src/ui/components.py
import pygame

class Button:
    def __init__(self, x, y, width, height, text, font, bg_color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.is_hovered = False

    def draw(self, surface):
        # Deteksi tabrakan (hover) kursor mouse
        mouse_pos = pygame.mouse.get_pos()
        self.is_hovered = self.rect.collidepoint(mouse_pos)

        color = self.hover_color if self.is_hovered else self.bg_color
        pygame.draw.rect(surface, color, self.rect, border_radius=8)

        # Render Teks
        text_surf = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered:
                return True
        return False
```

## Penggambaran Layar Game (Play Screen)

* **Timer Bar**: Digambar menggunakan `pygame.draw.rect()` dengan *width* yang dikurangi secara dinamis berbasis `pygame.time.get_ticks()`.
* **Nyawa (Lives)**: Digambar menggunakan *icon* hati (`assets/images/heart.png`) yang di-*blit* berjejer sebanyak `sisa_nyawa`.
* **Teks Soal Multiline**: Pygame standar tidak bisa *word-wrap* teks secara otomatis. Tim harus membuat fungsi *utility* (atau menggunakan fungsi tambahan) untuk memecah *string* soal yang panjang ke dalam *array* baris dan merendernya dengan pergeseran `y + font_height`.