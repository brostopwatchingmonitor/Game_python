import os

# ================= KOORDINAT DAN RESOLUSI WINDOW =================
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
DISPLAY_WIDTH, DISPLAY_HEIGHT = 400, 300  # Resolusi internal (skala 2x otomatis ke 800x600)
TILE_SIZE = 16  # Sesuai untuk grafik 16x16px
FRAMERATE = 60

# ================= WARNA (COLOR PALETTES) =================
BG_COLOR = '#fcdfcd'
COL_GOLD = (255, 210, 50)
COL_ACCENT = (0, 210, 200)
COL_WHITE = (255, 255, 255)
COL_BLACK = (0, 0, 0)
COL_DARK_GRAY = (30, 30, 30)
COL_RED = (220, 50, 50)

# ================= PATH DIREKTORI =================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')

# ================= KONSTANTA GAMEPLAY =================
XP_BASE = 100
PLAYER_MAX_HP = 100
PLAYER_ATTACK = 30
MOVE_SPEED = 120  # Disesuaikan agar pas dengan skala internal 400x300 (400 terlalu cepat untuk canvas 400px)
BULLET_COOLDOWN = 1500

# ================= GAME STATE KONSTANTA =================
STATE_INTRO       = "intro"
STATE_MENU        = "menu"
STATE_PLAYING     = "playing"
STATE_PAUSE       = "pause"
STATE_BOSS        = "boss"
STATE_STAGE_CLEAR = "stage_clear"
STATE_SHOP        = "shop"
STATE_GAME_OVER   = "game_over"
STATE_WIN         = "win"
STATE_MAP         = "map"
STATE_DIALOGUE    = "dialogue"
