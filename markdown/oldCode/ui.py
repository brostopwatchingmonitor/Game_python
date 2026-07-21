# ============================================================
#  src/ui.py — HUD, Menu, Game Over, Intro, Stage Clear (Full RPG)
# ============================================================

import pygame
import math
import settings


def _load_font(size, bold=False):
    try:    return pygame.font.SysFont("Segoe UI", size, bold=bold)
    except: return pygame.font.SysFont("Arial",    size, bold=bold)


class UI:
    INTRO_LINES = [
        "Sebuah dunia yang damai...",
        "Hancur oleh Lord HyperEnd.",
        "Hasumi — gadis remaja yang terdistorsi",
        "ruang dan waktu bersama reruntuhan dunianya,",
        "terdampar di kedalaman laut yang asing.",
        "",
        "Ia harus bertahan.",
        "Ia harus melawan.",
        "Ia harus menemukan jalan pulang.",
    ]

    def __init__(self):
        self._font_sm    = _load_font(18)
        self._font_md    = _load_font(24, bold=True)
        self._font_lg    = _load_font(42, bold=True)
        self._font_xl    = _load_font(68, bold=True)
        self._font_story = _load_font(21)
        self._font_hud   = _load_font(17, bold=True)

        # Intro typewriter
        self._intro_line  = 0
        self._intro_char  = 0
        self._intro_timer = 0
        self._intro_done  = False
        self._intro_hold  = 0

        # Menu & misc
        self._menu_tick   = 0
        self._lv_notif    = ""
        self._lv_timer    = 0

    # ── HUD ───────────────────────────────────────────────────
    def draw_hud(self, screen, player, score, stage, skill_manager):
        W = settings.SCREEN_WIDTH

        # Panel kiri
        panel = pygame.Surface((230, 155), pygame.SRCALPHA)
        panel.fill((0, 10, 30, 160))
        pygame.draw.rect(panel, (0, 160, 200, 80), panel.get_rect(), 1)
        screen.blit(panel, (8, 8))

        # HP bar
        self._draw_bar(screen, 18, 16, 200, 13,
                       player.hp, player.max_hp,
                       (220, 40, 60), (30, 10, 10), label="HP")
        # WP bar
        wp_col = (80, 160, 255) if not player._wp_exhausted else (255, 100, 60)
        self._draw_bar(screen, 18, 38, 200, 10,
                       player.wp, player.max_wp,
                       wp_col, (10, 15, 40), label="WP")

        # XP bar
        self._draw_bar(screen, 18, 56, 200, 7,
                       player.xp, player.xp_to_lv,
                       (80, 220, 255), (10, 20, 50))

        # Stats
        lv  = self._font_hud.render(f"Lv.{player.level}  ⚔{player.attack}  🪙{player.gold}", True, settings.COL_GOLD)
        screen.blit(lv, (18, 70))
        sc  = self._font_hud.render(f"Score: {score}", True, (180, 210, 240))
        screen.blit(sc, (18, 92))

        # Stage info
        if stage:
            ki_left = max(0, stage.kill_target - stage.kill_count)
            st = self._font_hud.render(
                f"Stage {stage.index+1}: {stage.name}  |  Kill: {stage.kill_count}/{stage.kill_target}",
                True, (120, 200, 240))
            screen.blit(st, (18, 114))

            # Kill progress bar
            self._draw_bar(screen, 18, 134, 200, 6,
                           stage.kill_count, stage.kill_target,
                           (0, 220, 180), (20, 40, 30))

        # WP Exhausted warning
        if player._wp_exhausted:
            w = int(math.sin(pygame.time.get_ticks() * 0.01) * 3)
            ws = self._font_md.render("⚠ KELELAHAN ⚠", True, (255, 100, 0))
            screen.blit(ws, (W//2 - ws.get_width()//2, 8 + w))

        # Skill HUD (pojok kanan atas)
        if skill_manager:
            self._draw_skill_hud(screen, skill_manager, player)

        # Level Up notif
        self.draw_level_up(screen)

        # Kontrol hint
        hints = ["←→/AD Gerak", "W/Spasi Lompat", "Z Tembak  X/C/V Skill"]
        for i, h in enumerate(hints):
            hs = self._font_sm.render(h, True, (70, 100, 130))
            screen.blit(hs, (W - 210, settings.SCREEN_HEIGHT - 56 + i*18))

    def _draw_bar(self, screen, x, y, w, h, val, max_val, col_fill, col_bg, label=""):
        ratio = max(0, val / max_val) if max_val > 0 else 0
        pygame.draw.rect(screen, col_bg,   (x, y, w, h))
        pygame.draw.rect(screen, col_fill, (x, y, int(w*ratio), h))
        pygame.draw.rect(screen, (100,100,100), (x, y, w, h), 1)
        if label:
            ls = self._font_sm.render(label, True, (200,200,200))
            screen.blit(ls, (x + 1, y - 1))

    def _draw_skill_hud(self, screen, skill_manager, player):
        # from src.skill import SKILL_KEYS
        import pygame
        W    = settings.SCREEN_WIDTH
        keys = ["X", "C", "V", "B"]
        sx   = W - 210
        sy   = 8
        for i, skill in enumerate(skill_manager.skills):
            if not skill.unlocked:
                continue
            bx = sx + i * 52
            # Kotak skill
            box = pygame.Surface((46, 46), pygame.SRCALPHA)
            if skill.ready:
                box.fill((0, 40, 60, 200))
                pygame.draw.rect(box, skill.COLOR + (200,), box.get_rect(), 2)
            else:
                box.fill((10, 10, 20, 200))
                pygame.draw.rect(box, (60, 60, 80, 150), box.get_rect(), 2)
                # Cooldown overlay
                cd_h = int(46 * (1 - skill.cd_ratio))
                overlay = pygame.Surface((46, cd_h), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 140))
                box.blit(overlay, (0, 0))
            screen.blit(box, (bx, sy))
            # Nama pendek
            short = skill.NAME.split()[0][:4]
            ns = self._font_sm.render(short, True, (200,220,240) if skill.ready else (80,80,100))
            screen.blit(ns, (bx + 2, sy + 3))
            # Tombol
            ks = self._font_sm.render(f"[{keys[i]}]", True, (140,160,180))
            screen.blit(ks, (bx + 2, sy + 26))
            # WP cost
            if skill.WP_COST > 0:
                wc = self._font_sm.render(f"{skill.WP_COST}wp", True, (80,140,255))
                screen.blit(wc, (bx + 2, sy + 42))

    # ── Boss HP Bar ───────────────────────────────────────────
    def draw_boss_bar(self, screen, boss):
        W   = settings.SCREEN_WIDTH
        bw  = W - 80
        bx  = 40
        by  = settings.SCREEN_HEIGHT - 48

        # Tentukan skema warna & simbol icon berdasarkan nama boss
        if "Crab" in boss.name:
            label_col = (255, 120, 40)
            prefix = "🦀 "
        elif "Shark" in boss.name:
            label_col = (80, 150, 240)
            prefix = "🦈 "
        else:
            label_col = (200, 0, 255)
            prefix = "☠ "

        panel = pygame.Surface((bw + 20, 38), pygame.SRCALPHA)
        panel.fill((20, 0, 40, 200) if "Warden" in boss.name else (10, 15, 30, 200))
        pygame.draw.rect(panel, label_col + (120,), panel.get_rect(), 2)
        screen.blit(panel, (bx - 10, by - 6))

        label = self._font_md.render(f"{prefix}{boss.name.upper()}", True, label_col)
        screen.blit(label, (bx, by - 4))

        ratio = boss.hp / boss.max_hp
        pygame.draw.rect(screen, (30, 10, 20) if "Warden" in boss.name else (15, 20, 30), (bx, by + 14, bw, 16))
        
        col = label_col if ratio > 0.3 else (255, 0, 80)
        pygame.draw.rect(screen, col, (bx, by + 14, int(bw*ratio), 16))
        pygame.draw.rect(screen, label_col, (bx, by + 14, bw, 16), 2)

        if boss.stage_idx >= 2:
            ph_col = [(0, 200, 200), (255, 160, 0), (255, 0, 80)][boss.phase - 1]
            ph = self._font_sm.render(f"Phase {boss.phase}", True, ph_col)
        else:
            ph = self._font_sm.render("MINI-BOSS", True, label_col)
        screen.blit(ph, (bx + bw - ph.get_width() - 4, by + 16))

    # ── Level Up ─────────────────────────────────────────────
    def show_level_up(self, level):
        self._lv_notif = f"✦ LEVEL UP!  Lv.{level} ✦"
        self._lv_timer = 120

    def draw_level_up(self, screen):
        if self._lv_timer <= 0:
            return
        self._lv_timer -= 1
        surf = self._font_lg.render(self._lv_notif, True, settings.COL_GOLD)
        surf.set_alpha(min(255, self._lv_timer * 4))
        screen.blit(surf, (settings.SCREEN_WIDTH//2 - surf.get_width()//2, 150))

    # ── Stage Clear ───────────────────────────────────────────
    def draw_stage_clear(self, screen, stage, score, player, time_elapsed):
        W, H = settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT
        overlay = pygame.Surface((W, H), pygame.SRCALPHA)
        overlay.fill((0, 5, 20, 210))
        screen.blit(overlay, (0, 0))

        # Judul
        t1 = self._font_xl.render("STAGE CLEAR!", True, (0, 255, 200))
        screen.blit(t1, (W//2 - t1.get_width()//2, 60))
        t2 = self._font_md.render(stage.name, True, (120, 200, 255))
        screen.blit(t2, (W//2 - t2.get_width()//2, 148))

        pygame.draw.line(screen, (0, 150, 180), (80, 182), (W-80, 182), 2)

        # Grade
        grade_cols = {"S": (255,220,0), "A": (0,220,255), "B": (0,200,80), "C": (180,180,180)}
        gcol = grade_cols.get(stage.grade, (255,255,255))
        gsurf = self._font_xl.render(stage.grade, True, gcol)
        screen.blit(gsurf, (W//2 - gsurf.get_width()//2, 195))

        # Stats
        secs = int(time_elapsed)
        lines = [
            f"Kill       :  {stage.kill_count}",
            f"Waktu      :  {secs // 60}m {secs % 60}s",
            f"HP Tersisa :  {player.hp} / {player.max_hp}",
            f"Gold Dapat :  +{player.gold}",
            f"Score      :  {score}",
        ]
        for i, l in enumerate(lines):
            s = self._font_md.render(l, True, (190, 215, 240))
            screen.blit(s, (W//2 - 160, 290 + i*38))

        # Tombol
        c1 = self._font_md.render("[ ENTER ]  Lanjut ke Toko", True, settings.COL_ACCENT)
        screen.blit(c1, (W//2 - c1.get_width()//2, H - 65))

    # ── Intro ─────────────────────────────────────────────────
    def update_intro(self):
        if self._intro_done:
            return True
        self._intro_timer += 1
        if self._intro_hold > 0:
            self._intro_hold -= 1
            return False
        current = self.INTRO_LINES[self._intro_line]
        if self._intro_char < len(current):
            if self._intro_timer % 2 == 0:
                self._intro_char += 1
        else:
            self._intro_hold = 40
            self._intro_line += 1
            self._intro_char  = 0
            if self._intro_line >= len(self.INTRO_LINES):
                self._intro_done = True
        return False

    def draw_intro(self, screen):
        import random
        W, H = settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT
        screen.fill((2, 5, 15))
        rng = random.Random(42)
        for _ in range(80):
            sx = rng.randint(0, W); sy = rng.randint(0, H//2); r = rng.randint(1,3)
            pygame.draw.circle(screen, (200,180,255), (sx,sy), r)
        title = self._font_lg.render("HASUMI", True, (0, 220, 200))
        sub   = self._font_sm.render("Beneath the Shattered Sky", True, (100,160,220))
        screen.blit(title, (W//2 - title.get_width()//2, 28))
        screen.blit(sub,   (W//2 - sub.get_width()//2,   80))
        pygame.draw.line(screen, (0,100,120), (80,108), (W-80,108), 1)
        start_y = 130
        for i in range(self._intro_line):
            if i < len(self.INTRO_LINES):
                ts = self._font_story.render(self.INTRO_LINES[i], True, (180,220,255))
                screen.blit(ts, (W//2 - ts.get_width()//2, start_y + i*32))
        if self._intro_line < len(self.INTRO_LINES):
            partial = self.INTRO_LINES[self._intro_line][:self._intro_char]
            ts = self._font_story.render(partial, True, (220,240,255))
            screen.blit(ts, (W//2 - ts.get_width()//2, start_y + self._intro_line*32))
            if (pygame.time.get_ticks()//400)%2 == 0:
                cx = W//2 - ts.get_width()//2 + ts.get_width() + 3
                cy = start_y + self._intro_line*32
                pygame.draw.rect(screen, (0,220,200), (cx, cy+3, 2, 16))
        if self._intro_done:
            sk = self._font_md.render("[ ENTER ] Mulai Petualangan", True, settings.COL_ACCENT)
        else:
            sk = self._font_sm.render("[ ENTER ] Skip", True, (70,90,110))
        screen.blit(sk, (W//2 - sk.get_width()//2, H - 48))

    # ── Menu ──────────────────────────────────────────────────
    def draw_menu(self, screen, has_save=False):
        import random
        W, H = settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT
        self._menu_tick += 1
        for y in range(H):
            t = y/H
            pygame.draw.line(screen, (int(5+t*15), int(20+t*50), int(55+t*80)), (0,y),(W,y))
        wave = int(math.sin(self._menu_tick*0.05)*5)
        t1 = self._font_xl.render("HASUMI", True, (0,220,200))
        t2 = self._font_md.render("Beneath the Shattered Sky", True, (120,180,255))
        screen.blit(t1, (W//2 - t1.get_width()//2, 110+wave))
        screen.blit(t2, (W//2 - t2.get_width()//2, 200+wave))
        pygame.draw.line(screen, (0,140,170), (100,238),(W-100,238), 2)
        items = ["[ ENTER ]  Mulai Baru"]
        if has_save:
            items.append("[ L ]      Lanjutkan")
        items.append("[ ESC ]    Keluar")
        cols  = [settings.COL_ACCENT, (0,220,160), (160,160,180)]
        for i, item in enumerate(items):
            surf = self._font_md.render(item, True, cols[i] if i < len(cols) else (180,180,200))
            screen.blit(surf, (W//2 - surf.get_width()//2, 268 + i*56))
        cr = self._font_sm.render("Terinspirasi dari Mission Mermaiden ~Hasumi~", True, (45,70,95))
        screen.blit(cr, (W//2 - cr.get_width()//2, H-32))

    # ── Game Over ─────────────────────────────────────────────
    def draw_game_over(self, screen, score, kill_count, level):
        W, H = settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT
        overlay = pygame.Surface((W,H), pygame.SRCALPHA)
        overlay.fill((0,0,0,190))
        screen.blit(overlay, (0,0))
        go = self._font_xl.render("GAME OVER", True, (220,30,60))
        screen.blit(go, (W//2 - go.get_width()//2, H//2 - 140))
        pygame.draw.line(screen, (180,0,60), (120,H//2-80),(W-120,H//2-80), 2)
        for i, l in enumerate([f"Score : {score}", f"Kill  : {kill_count}", f"Level : {level}"]):
            s = self._font_md.render(l, True, (200,210,230))
            screen.blit(s, (W//2 - s.get_width()//2, H//2-45 + i*38))
        r = self._font_md.render("[ R ]  Coba Lagi", True, (0,220,180))
        screen.blit(r, (W//2 - r.get_width()//2, H//2+80))
        m = self._font_md.render("[ M ]  Menu Utama", True, (150,150,180))
        screen.blit(m, (W//2 - m.get_width()//2, H//2+118))

    # ── Win ───────────────────────────────────────────────────
    def draw_win(self, screen, score, kill_count, level):
        W, H = settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT
        self._menu_tick += 1
        overlay = pygame.Surface((W,H), pygame.SRCALPHA)
        overlay.fill((0,5,20,210))
        screen.blit(overlay, (0,0))
        wave = int(math.sin(self._menu_tick*0.06)*6)
        t1 = self._font_xl.render("MENANG!", True, (255,220,0))
        t2 = self._font_md.render("Lord HyperEnd dikalahkan!", True, (0,220,200))
        screen.blit(t1, (W//2 - t1.get_width()//2, H//2-150+wave))
        screen.blit(t2, (W//2 - t2.get_width()//2, H//2-80))
        for i, l in enumerate([f"Score : {score}", f"Kill  : {kill_count}", f"Level : {level}"]):
            s = self._font_md.render(l, True, (200,230,255))
            screen.blit(s, (W//2 - s.get_width()//2, H//2-15 + i*38))
        r = self._font_md.render("[ R ]  Main Lagi", True, (255,220,0))
        screen.blit(r, (W//2 - r.get_width()//2, H//2+108))
