# ============================================================
#  src/dialogue.py — Sistem Dialog Visual Novel & Potret Karakter
# ============================================================

import pygame
import math
import os
import settings

# --- Data Naskah Dialog (Cutscenes) ---
DIALOGUE_SCRIPTS = {
    # ── Stage 1: Sebelum Mulai ──
    "intro_stage_0": [
        {"speaker": "Hasumi", "side": "left", "emotion": "worried", "text": "Di mana ini? Airnya terasa begitu dingin... dan langitnya tampak hancur."},
        {"speaker": "Saki", "side": "right", "emotion": "idle", "text": "Identifikasi terdeteksi. Entitas non-terdistorsi. Siapa kamu?"},
        {"speaker": "Hasumi", "side": "left", "emotion": "worried", "text": "Aku Hasumi. Aku terlempar dari duniaku saat badai merusak segalanya."},
        {"speaker": "Saki", "side": "right", "emotion": "smile", "text": "Aku Saki, yah aku adalah salah satu pelindung di kawasan ini dari makhluk ataupun entitas abstrak dan berbahaya."},
        {"speaker": "Saki", "side": "left", "emotion": "serious", "text": "Dan kamu apa yang bisa membuktikan bahwa kamu bukan ancaman? kamu benar benar terlihat tidak seperti gadis biasa"},
        {"speaker": "Hasumi", "side": "left", "emotion": "worried", "text": "Aku... aku memang bukan gadis biasa tapi bukan berarti aku ancaman!"},
        {"speaker": "Saki", "side": "right", "emotion": "idle", "text": "hmmmh... baiklah mari kita lihat apa kamu bukan ancaman dengan mengalahkan beberapa monster itu!"},
        {"speaker": "Hasumi", "side": "left", "emotion": "worried", "text": "H-HAH?! Tapi-"},
        {"speaker": "Saki", "side": "right", "emotion": "smile", "text": "selamat mencoba dan jangan terluka ya~"},
    ],
    # ── Stage 1: Setelah Selesai ──
    "clear_stage_0": [
        {"speaker": "Saki", "side": "right", "emotion": "smile", "text": "ohh... Boleh tahan, kamu punya potensi yang cukup bagus untuk seorang pendatang baru."},
        {"speaker": "Hasumi", "side": "left", "emotion": "smile", "text": "Hah? Kamu Gila ya!"},
        {"speaker": "Saki", "side": "right", "emotion": "idle", "text": "ssshhh... cukup sampai disini, kamu sudah menunjukan sedikit banyaknya kemampuanmu, baiklah kamu bisa ikut aku ke tempat selanjutnya."},
        {"speaker": "Hasumi", "side": "left", "emotion": "worried", "text": "huft... ampun deh..."},
        {"speaker": "Saki", "side": "right", "emotion": "smile", "text": "Sebelum lanjut, mampirlah ke Toko Laut Dalam. Aku bisa membantumu meningkatkan kekuatan!"}
    ],
    # ── Stage 2: Sebelum Mulai ──
    "intro_stage_1": [
        {"speaker": "Hasumi", "side": "left", "emotion": "worried", "text": "Gelap sekali di bawah sini... Aku bahkan sulit melihat ujung siripku."},
        {"speaker": "Saki", "side": "right", "emotion": "idle", "text": "Tekanan laut dalam terdeteksi. Hiu-hiu di area ini sangat agresif dan bisa menembak."},
        {"speaker": "Hasumi", "side": "left", "emotion": "smile", "text": "Aku tidak akan menyerah. Aku merasakan energi hangat di dasar laut ini."},
        {"speaker": "Saki", "side": "right", "emotion": "smile", "text": "Itu adalah inti kehidupan laut yang tersisa. Selamatkan mereka, Hasumi!"}
    ],
    # ── Stage 2: Setelah Selesai ──
    "clear_stage_1": [
        {"speaker": "Hasumi", "side": "left", "emotion": "idle", "text": "Hampir saja... monster hiu tadi benar-benar merepotkan."},
        {"speaker": "Saki", "side": "right", "emotion": "worried", "text": "Peringatan! Sinyal energi Lord HyperEnd meledak di kedalaman berikutnya."},
        {"speaker": "Saki", "side": "right", "emotion": "idle", "text": "Tahap akhir ada di depan kita. Sarang HyperEnd. Bersiaplah dengan matang."}
    ],
    # ── Stage 3: Sebelum Mulai ──
    "intro_stage_2": [
        {"speaker": "Saki", "side": "right", "emotion": "worried", "text": "Hasumi, energi di sini sangat merusak. Willpower (WP) kamu akan lebih cepat terkuras jika terkena hit."},
        {"speaker": "Hasumi", "side": "left", "emotion": "smile", "text": "Aku merasakannya. Tapi tekadku untuk mengembalikan langit yang hancur tidak akan goyah!"},
        {"speaker": "Saki", "side": "right", "emotion": "smile", "text": "Bagus. Aku akan mengawasi portal pelarian dari sini. Hancurkan Sarang Void Core itu!"}
    ],
    # ── Stage 3: Setelah Selesai / Boss Intro ──
    "clear_stage_2": [
        {"speaker": "Lord HyperEnd", "side": "right", "emotion": "angry", "text": "Mermaid kecil yang berisik... Beraninya kau menembus sarang Void Core-ku!"},
        {"speaker": "Hasumi", "side": "left", "emotion": "angry", "text": "Kau yang merusak lautan dan memecah belah langit! Aku akan menghentikanmu di sini!"},
        {"speaker": "Lord HyperEnd", "side": "right", "emotion": "angry", "text": "Hahaha! Lautan ini akan tenggelam dalam kehampaan abadi. Hadapi murka Void Core!"}
    ],
    # ── Ending / Win Dialogue ──
    "win_ending": [
        {"speaker": "Lord HyperEnd", "side": "right", "emotion": "angry", "text": "T-Tidak mungkin! Energi cahayamu... menghancurkan kehampaan ku..."},
        {"speaker": "Hasumi", "side": "left", "emotion": "smile", "text": "Akhirnya... cahayanya kembali. Lautan terasa hangat lagi."},
        {"speaker": "Saki", "side": "right", "emotion": "smile", "text": "Kerja bagus, Hasumi! Portal dimensi telah terbuka kembali. Langit di atas mulai menyatu."},
        {"speaker": "Saki", "side": "right", "emotion": "smile", "text": "Saatnya kamu pulang ke duniamu yang indah. Selamat tinggal, pahlawan laut!"},
        {"speaker": "Hasumi", "side": "left", "emotion": "smile", "text": "Selamat tinggal Saki, terima kasih atas bantuannya! Aku tidak akan melupakan petualangan ini."}
    ]
}


def _load_font(size, bold=False):
    try:    return pygame.font.SysFont("Segoe UI", size, bold=bold)
    except: return pygame.font.SysFont("Arial",    size, bold=bold)


# ── Memuat sequence sprite dari folder ─────────────────────────
def _load_sequence(folder, filenames, target_h):
    """Muat daftar berkas gambar dari folder dan scale sesuai target_h."""
    frames = []
    for fname in filenames:
        path = os.path.join(folder, fname)
        if os.path.isfile(path):
            try:
                img = pygame.image.load(path).convert_alpha()
                orig_w, orig_h = img.get_size()
                scale = target_h / orig_h
                new_w = int(orig_w * scale)
                img = pygame.transform.scale(img, (new_w, target_h))
                frames.append(img)
            except Exception as e:
                print(f"[dialogue] Error loading {path}: {e}")
    return frames


class DialogueManager:
    """Mengatur alur dialog VN, potret karakter sprite, dan visual textbox neon."""

    # Tinggi portrait karakter di layar dialog (dalam piksel)
    PORTRAIT_H = 420

    def __init__(self):
        self._font_name  = _load_font(22, bold=True)
        self._font_text  = _load_font(20)
        self._font_hint  = _load_font(15)

        self.current_script = []
        self.line_idx       = 0
        self.char_idx       = 0
        self.text_timer     = 0
        self.active         = False
        self.on_complete_cb = None

        # Animasi portrait
        self._anim_tick  = 0
        self._anim_frame = 0

        # Cache potret geometris (fallback)
        self._portrait_cache = {}

        # Muat sprite portrait dari aset
        self._hasumi_idle    = []
        self._saki_idle      = []
        self._load_portrait_sprites()

    def _load_portrait_sprites(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        aset_dir = os.path.join(base_dir, "..", "data", "assets_p1", "aset_karakter_Hasumi")
        h = self.PORTRAIT_H

        # Hasumi: front_idle sequence
        self._hasumi_idle = _load_sequence(
            aset_dir,
            [f"front_idle_{i}.png" for i in range(4)],
            h
        )
        # Fallback: idle_right
        if not self._hasumi_idle:
            self._hasumi_idle = _load_sequence(
                aset_dir,
                [f"idle_right{i}.png" for i in range(4)],
                h
            )

        # Saki: Muat dari Asset_Saki jika ada, jika tidak, fallback ke aset Hasumi
        saki_new_dir = os.path.join(base_dir, "..", "data", "assets_p1", "Asset_Saki")
        saki_new_file = "—Pngtree—game character anime comic girl_3932788.png"
        saki_new_path = os.path.join(saki_new_dir, saki_new_file)

        self._saki_idle = []
        if os.path.isfile(saki_new_path):
            try:
                img = pygame.image.load(saki_new_path).convert_alpha()
                bbox = img.get_bounding_rect()
                cropped = img.subsurface(bbox)
                
                orig_w, orig_h = cropped.get_size()
                scale = h / orig_h
                new_w = int(orig_w * scale)
                scaled_base = pygame.transform.scale(cropped, (new_w, h))

                # Buat 4 frame animasi pernapasan (idle breathing)
                self._saki_idle = [
                    scaled_base,  # Frame 0: normal
                    pygame.transform.scale(scaled_base, (int(new_w * 0.99), int(h * 1.01))), # Frame 1: breathing
                    pygame.transform.scale(scaled_base, (int(new_w * 0.985), int(h * 1.015))), # Frame 2: peak inhale
                    pygame.transform.scale(scaled_base, (int(new_w * 0.99), int(h * 1.01)))  # Frame 3: exhale
                ]
                print("[dialogue] Successfully loaded Saki's new premium design from Asset_Saki!")
            except Exception as e:
                print(f"[dialogue] Error loading premium Saki asset: {e}")

        # Fallback jika gagal atau tidak ditemukan
        if not self._saki_idle:
            self._saki_idle = _load_sequence(
                aset_dir,
                [f"idle_left{i}.png" for i in range(4)],
                h
            )

    # ── Lifecycle ─────────────────────────────────────────────
    def start_cutscene(self, script_key, on_complete_callback=None):
        if script_key in DIALOGUE_SCRIPTS:
            self.current_script = DIALOGUE_SCRIPTS[script_key]
            self.line_idx       = 0
            self.char_idx       = 0
            self.text_timer     = 0
            self.active         = True
            self.on_complete_cb = on_complete_callback
            self._anim_frame    = 0
            self._anim_tick     = 0
            return True
        return False

    def handle_key(self, key):
        if not self.active:
            return
        if key == pygame.K_RETURN or key == pygame.K_z:
            current_line = self.current_script[self.line_idx]
            if self.char_idx < len(current_line["text"]):
                self.char_idx = len(current_line["text"])
            else:
                self.line_idx += 1
                self.char_idx = 0
                if self.line_idx >= len(self.current_script):
                    self.active = False
                    if self.on_complete_cb:
                        self.on_complete_cb()
        elif key == pygame.K_ESCAPE:
            self.active = False
            if self.on_complete_cb:
                self.on_complete_cb()

    def update(self):
        if not self.active:
            return
        current_line = self.current_script[self.line_idx]
        self.text_timer += 1
        if self.text_timer >= 2:
            self.text_timer = 0
            if self.char_idx < len(current_line["text"]):
                self.char_idx += 1

        # Animasi portrait idle (ganti frame tiap 18 frame)
        self._anim_tick += 1
        if self._anim_tick >= 18:
            self._anim_tick = 0
            self._anim_frame += 1

    # ── Draw ──────────────────────────────────────────────────
    def draw(self, screen):
        if not self.active:
            return

        current_line = self.current_script[self.line_idx]
        speaker  = current_line["speaker"]
        emotion  = current_line.get("emotion", "idle")

        W, H = settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT

        # ── 1. Render Portrait Karakter ──
        self._draw_portraits(screen, speaker, emotion)

        # ── 2. Semi-transparan gradient bawah ──
        gradient = pygame.Surface((W, 200), pygame.SRCALPHA)
        for i in range(200):
            alpha = int(180 * (i / 200))
            pygame.draw.line(gradient, (0, 5, 15, alpha), (0, i), (W, i))
        screen.blit(gradient, (0, H - 200))

        # ── 3. Text Box Utama ──
        bx, by = 30, H - 175
        bw, bh = W - 60, 145

        box_surf = pygame.Surface((bw, bh), pygame.SRCALPHA)
        # Latar belakang box gradient
        for i in range(bh):
            alpha = int(200 + 40 * (i / bh))
            pygame.draw.line(box_surf, (0, 8, 22, min(alpha, 235)), (0, i), (bw, i))
        # Border neon lapis ganda
        pygame.draw.rect(box_surf, (0, 190, 255, 200), box_surf.get_rect(), 2)
        pygame.draw.rect(box_surf, (0, 255, 230, 60),
                         pygame.Rect(3, 3, bw - 6, bh - 6), 1)
        screen.blit(box_surf, (bx, by))

        # ── 4. Name Plate ──
        nx, ny = bx + 16, by - 30
        nw, nh = max(180, self._font_name.size(speaker)[0] + 32), 34

        name_surf = pygame.Surface((nw, nh), pygame.SRCALPHA)
        # Gradient diagonal nama
        for i in range(nh):
            alpha = int(230 - 30 * (i / nh))
            pygame.draw.line(name_surf, (0, 12, 30, alpha), (0, i), (nw, i))
        pygame.draw.rect(name_surf, (0, 200, 200, 200), name_surf.get_rect(), 2)
        screen.blit(name_surf, (nx, ny))

        # Warna nama berdasarkan karakter
        if speaker == "Hasumi":
            name_col = (255, 230, 100)
        elif speaker == "Saki":
            name_col = (0, 255, 220)
        elif "Lord" in speaker:
            name_col = (220, 50, 255)
        else:
            name_col = (255, 255, 255)

        ns = self._font_name.render(speaker, True, name_col)
        screen.blit(ns, (nx + 12, ny + 5))

        # Garis dekoratif di bawah nameplate
        pygame.draw.line(screen, (0, 180, 200, 160),
                         (nx, ny + nh), (nx + nw, ny + nh), 1)

        # ── 5. Isi Teks (Typewriter Effect + Word Wrap) ──
        full_text    = current_line["text"]
        visible_text = full_text[:self.char_idx]
        lines = self._wrap_text(visible_text, self._font_text, bw - 50)

        for i, line in enumerate(lines[:4]):
            col = (230, 245, 255) if i < len(lines) - 1 or self.char_idx >= len(full_text) else (255, 255, 255)
            ts = self._font_text.render(line, True, col)
            screen.blit(ts, (bx + 26, by + 22 + i * 28))

        # ── 6. Indikator Lanjut (▼ blink) ──
        if self.char_idx >= len(full_text):
            if (pygame.time.get_ticks() // 400) % 2 == 0:
                tri_x = bx + bw - 30
                tri_y = by + bh - 18
                pygame.draw.polygon(screen, (0, 220, 255),
                                    [(tri_x, tri_y), (tri_x + 10, tri_y), (tri_x + 5, tri_y + 8)])

        hint = self._font_hint.render("[ ENTER / Z ] Lanjut    [ ESC ] Lewati",
                                       True, (60, 100, 130))
        screen.blit(hint, (W - hint.get_width() - 50, by + bh - 20))

    # ── Render Portrait Sprite
    def _draw_portraits(self, screen, active_speaker, emotion):
        W, H = settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT
        ph    = self.PORTRAIT_H

        # main char gwe selalu di kiri
        hasumi_active = (active_speaker == "Hasumi")
        right_active  = not hasumi_active

        # ── Potret Hasumi (Kiri) ──
        if self._hasumi_idle:
            frame_idx  = self._anim_frame % len(self._hasumi_idle)
            frame      = self._hasumi_idle[frame_idx]
            pw         = frame.get_width()
            dest_x     = 40
            dest_y     = H - ph - 10

            if hasumi_active:
                # Karakter aktif: efek bobbing halus + glowing
                bob = int(math.sin(pygame.time.get_ticks() * 0.003) * 4)
                rendered = frame
                glow_surf = pygame.Surface((pw + 20, 20), pygame.SRCALPHA)
                pygame.draw.ellipse(glow_surf, (0, 210, 255, 60), glow_surf.get_rect())
                screen.blit(glow_surf, (dest_x - 10, dest_y + ph - 10))
                screen.blit(rendered, (dest_x, dest_y + bob))
            else:
                # Karakter yg gak ngomong gelapin
                dark = frame.copy()
                dark.fill((0, 0, 0, 110), special_flags=pygame.BLEND_RGBA_MULT)
                screen.blit(dark, (dest_x, dest_y))
        else:
            # Fallback buat render
            hasumi_x = 80
            hasumi_y = H - 430
            self._render_hasumi_geo(screen, hasumi_x, hasumi_y,
                                    active=hasumi_active, emotion=emotion)

        #
        if "Lord" in active_speaker or (not hasumi_active and active_speaker == "Lord HyperEnd"):
            right_key = "lord"
        else:
            right_key = "saki"

        if right_key == "saki" and self._saki_idle:
            frame_idx = self._anim_frame % len(self._saki_idle)
            frame     = self._saki_idle[frame_idx]
            # Balik horizontal WOI
            frame     = pygame.transform.flip(frame, True, False)
            pw        = frame.get_width()
            ph_frame  = frame.get_height()
            dest_x    = W - pw - 40
            dest_y    = H - ph_frame - 10

            if right_active:
                bob = int(math.sin(pygame.time.get_ticks() * 0.003 + 1.5) * 4)
                glow_surf = pygame.Surface((pw + 20, 20), pygame.SRCALPHA)
                pygame.draw.ellipse(glow_surf, (255, 80, 200, 50), glow_surf.get_rect())
                screen.blit(glow_surf, (dest_x - 10, dest_y + ph_frame - 10))
                screen.blit(frame, (dest_x, dest_y + bob))
            else:
                dark = frame.copy()
                dark.fill((0, 0, 0, 110), special_flags=pygame.BLEND_RGBA_MULT)
                screen.blit(dark, (dest_x, dest_y))
        else:
           
            right_x = W - 320
            right_y = H - 430
            if right_key == "lord":
                self._render_lord_hyperend_geo(screen, right_x, right_y, active=right_active)
            else:
                self._render_saki_geo(screen, right_x, right_y,
                                      active=right_active, emotion=emotion)

    # ── Word Wrap Helper
    def _wrap_text(self, text, font, max_width):
        words = text.split(" ")
        lines = []
        current = ""
        for word in words:
            test = (current + " " + word).strip()
            if font.size(test)[0] <= max_width:
                current = test
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
        return lines

    def _render_hasumi_geo(self, screen, x, y, active, emotion):
        key = f"hasumi_geo_{emotion}_{active}"
        if key in self._portrait_cache:
            screen.blit(self._portrait_cache[key], (x, y))
            return
        surf = pygame.Surface((240, 320), pygame.SRCALPHA)
        pygame.draw.ellipse(surf, (255, 210, 180), (70, 60, 100, 110))
        pygame.draw.ellipse(surf, (100, 30, 120), (55, 50, 130, 140))
        pygame.draw.polygon(surf, (120, 35, 140), [(55, 120), (70, 240), (85, 120)])
        pygame.draw.polygon(surf, (120, 35, 140), [(155, 120), (170, 240), (185, 120)])
        pygame.draw.polygon(surf, (130, 45, 150), [(70, 70), (95, 110), (110, 70)])
        pygame.draw.polygon(surf, (130, 45, 150), [(110, 70), (125, 110), (145, 70)])
        pygame.draw.circle(surf, (0, 220, 200), (70, 65), 10)
        pygame.draw.circle(surf, (0, 220, 200), (170, 65), 10)
        eye_y = 105
        pygame.draw.ellipse(surf, (20, 80, 220), (85, eye_y, 16, 22))
        pygame.draw.ellipse(surf, (255, 255, 255), (89, eye_y + 3, 6, 8))
        pygame.draw.ellipse(surf, (20, 80, 220), (135, eye_y, 16, 22))
        pygame.draw.ellipse(surf, (255, 255, 255), (139, eye_y + 3, 6, 8))
        if emotion == "smile":
            pygame.draw.arc(surf, (150, 40, 60), (110, 125, 20, 15), math.pi, 2*math.pi, 3)
        elif emotion == "worried":
            pygame.draw.line(surf, (150, 40, 60), (112, 135), (128, 132), 3)
            pygame.draw.line(surf, (60, 20, 80), (82, 92), (98, 98), 2)
            pygame.draw.line(surf, (60, 20, 80), (138, 98), (154, 92), 2)
        else:
            pygame.draw.line(surf, (150, 40, 60), (112, 132), (128, 132), 2)
            pygame.draw.line(surf, (60, 20, 80), (82, 95), (98, 95), 2)
            pygame.draw.line(surf, (60, 20, 80), (138, 95), (154, 95), 2)
        pygame.draw.ellipse(surf, (255, 150, 150, 80), (80, 120, 20, 10))
        pygame.draw.ellipse(surf, (255, 150, 150, 80), (140, 120, 20, 10))
        pygame.draw.polygon(surf, (255, 210, 180), [(105, 160), (120, 185), (135, 160)])
        pygame.draw.ellipse(surf, (0, 30, 80), (60, 180, 120, 140))
        pygame.draw.line(surf, (0, 220, 200), (90, 180), (90, 320), 4)
        pygame.draw.line(surf, (0, 220, 200), (150, 180), (150, 320), 4)
        final_surf = pygame.Surface((240, 320), pygame.SRCALPHA)
        final_surf.blit(surf, (0, 0))
        if not active:
            overlay = pygame.Surface((240, 320), pygame.SRCALPHA)
            overlay.fill((20, 30, 50, 120))
            final_surf.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
        self._portrait_cache[key] = final_surf
        screen.blit(final_surf, (x, y))

    def _render_saki_geo(self, screen, x, y, active, emotion):
        key = f"saki_geo_{emotion}_{active}"
        if key in self._portrait_cache:
            screen.blit(self._portrait_cache[key], (x, y))
            return
        surf = pygame.Surface((240, 320), pygame.SRCALPHA)
        pygame.draw.polygon(surf, (255, 50, 120, 200), [(50, 120), (10, 80), (20, 140), (50, 160)])
        pygame.draw.polygon(surf, (255, 120, 0, 180), [(50, 100), (0, 40), (10, 90)])
        pygame.draw.polygon(surf, (255, 50, 120, 200), [(190, 120), (230, 80), (220, 140), (190, 160)])
        pygame.draw.polygon(surf, (255, 120, 0, 180), [(190, 100), (240, 40), (230, 90)])
        pygame.draw.ellipse(surf, (255, 215, 185), (70, 60, 100, 110))
        pygame.draw.ellipse(surf, (50, 10, 70), (55, 50, 130, 130))
        pygame.draw.ellipse(surf, (65, 12, 85), (35, 90, 45, 200))
        pygame.draw.ellipse(surf, (65, 12, 85), (160, 90, 45, 200))
        pygame.draw.polygon(surf, (80, 20, 100), [(70, 70), (95, 105), (110, 70)])
        pygame.draw.polygon(surf, (80, 20, 100), [(110, 70), (125, 105), (145, 70)])
        pygame.draw.circle(surf, (255, 100, 0), (62, 75), 8)
        pygame.draw.circle(surf, (255, 100, 0), (178, 75), 8)
        eye_y = 105
        pygame.draw.ellipse(surf, (255, 50, 50), (85, eye_y, 16, 22))
        pygame.draw.circle(surf, (255, 210, 0), (93, eye_y + 11), 3)
        pygame.draw.ellipse(surf, (255, 50, 50), (135, eye_y, 16, 22))
        pygame.draw.circle(surf, (255, 210, 0), (143, eye_y + 11), 3)
        if emotion == "smile":
            pygame.draw.arc(surf, (160, 30, 80), (110, 125, 20, 15), math.pi, 2*math.pi, 3)
        elif emotion == "worried":
            pygame.draw.line(surf, (160, 30, 80), (112, 135), (128, 133), 3)
            pygame.draw.line(surf, (80, 20, 110), (82, 92), (98, 98), 2)
            pygame.draw.line(surf, (80, 20, 110), (138, 98), (154, 92), 2)
        else:
            pygame.draw.line(surf, (160, 30, 80), (112, 132), (128, 132), 2)
            pygame.draw.line(surf, (80, 20, 110), (82, 95), (98, 95), 2)
            pygame.draw.line(surf, (80, 20, 110), (138, 95), (154, 95), 2)
        pygame.draw.polygon(surf, (255, 215, 185), [(105, 160), (120, 182), (135, 160)])
        pygame.draw.ellipse(surf, (30, 30, 45), (60, 180, 120, 150))
        pygame.draw.ellipse(surf, (220, 30, 120), (75, 195, 90, 130))
        final_surf = pygame.Surface((240, 320), pygame.SRCALPHA)
        final_surf.blit(surf, (0, 0))
        if not active:
            overlay = pygame.Surface((240, 320), pygame.SRCALPHA)
            overlay.fill((20, 30, 50, 120))
            final_surf.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
        self._portrait_cache[key] = final_surf
        screen.blit(final_surf, (x, y))

    def _render_lord_hyperend_geo(self, screen, x, y, active):
        key = f"lord_geo_{active}"
        if key in self._portrait_cache:
            screen.blit(self._portrait_cache[key], (x, y))
            return
        surf = pygame.Surface((260, 340), pygame.SRCALPHA)
        for r in range(5, 50, 10):
            pygame.draw.ellipse(surf, (100, 0, 160, 35 - r//2), (20-r, 30-r, 220+r*2, 260+r*2))
        pygame.draw.ellipse(surf, (15, 5, 30), (40, 40, 180, 250))
        pygame.draw.polygon(surf, (40, 0, 70), [(80, 50), (40, 0), (105, 45)])
        pygame.draw.polygon(surf, (40, 0, 70), [(180, 50), (220, 0), (155, 45)])
        pygame.draw.circle(surf, (255, 0, 80), (100, 120), 8)
        pygame.draw.circle(surf, (255, 255, 255), (100, 120), 3)
        pygame.draw.circle(surf, (255, 0, 80), (160, 120), 8)
        pygame.draw.circle(surf, (255, 255, 255), (160, 120), 3)
        pygame.draw.circle(surf, (255, 0, 80), (130, 95), 10)
        pygame.draw.circle(surf, (255, 255, 100), (130, 95), 4)
        pygame.draw.line(surf, (180, 0, 255), (100, 160), (130, 220), 4)
        pygame.draw.line(surf, (180, 0, 255), (160, 160), (130, 220), 4)
        pygame.draw.line(surf, (180, 0, 255), (130, 220), (130, 300), 5)
        final_surf = pygame.Surface((260, 340), pygame.SRCALPHA)
        final_surf.blit(surf, (0, 0))
        if not active:
            overlay = pygame.Surface((260, 340), pygame.SRCALPHA)
            overlay.fill((30, 10, 40, 140))
            final_surf.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
        self._portrait_cache[key] = final_surf
        screen.blit(final_surf, (x, y - 20))

