# Rancangan 2: Struktur Folder & Routing Logic

Menggunakan arsitektur modular untuk Pygame agar kode tidak menumpuk di dalam satu file `main.py`.

## Pohon Struktur Folder

```text
mindmatrix_game/
│
├── data/
│   ├── questions.json          # Bank soal
│   └── leaderboard.json        # Data skor pemain
│
├── docs/                       # Konfigurasi Sphinx & file reST (.rst)
│
├── assets/                     # Resource multimedia
│   ├── fonts/
│   ├── images/
│   └── sounds/
│
├── src/
│   ├── __init__.py
│   ├── main.py                 # Pygame Game Loop utama
│   ├── config.py               # Konstanta (WIDTH, HEIGHT, FPS, COLORS)
│   │
│   ├── core/                   # Logika game (skor, nyawa, timer)
│   │   ├── game_state.py
│   │   └── question_mgr.py
│   │
│   ├── database/               # DAO (Data Access Object) untuk JSON
│   │   └── json_manager.py
│   │
│   └── ui/
│       ├── components.py       # Kelas Button & Text Pygame
│       ├── state_manager.py    # Routing logic (FSM)
│       └── screens/
│           ├── menu_screen.py
│           ├── play_screen.py
│           └── score_screen.py
│
├── tests/
├── .gitignore
├── requirements.txt
└── README.md
```

## Routing Logic (Finite State Machine / FSM)

Dalam Pygame, *routing* antar modul tidak dilakukan dengan menutup jendela, melainkan mengubah "Status" (State) apa yang sedang di-*render* dan di-*update* di dalam Game Loop.

```python
# src/ui/state_manager.py

class GameStateManager:
    def __init__(self):
        self.states = {}
        self.current_state = None

    def add_state(self, state_name, state_object):
        self.states[state_name] = state_object

    def change_state(self, state_name):
        self.current_state = self.states[state_name]
        self.current_state.on_enter() # Fungsi inisialisasi saat layar dibuka

    def update(self, events):
        if self.current_state:
            self.current_state.update(events)

    def draw(self, surface):
        if self.current_state:
            self.current_state.draw(surface)

```

**Alur Kerja Game Loop (`main.py`):**
Loop utama hanya akan memanggil `state_manager.update(events)` dan `state_manager.draw(screen)`. State apa pun yang sedang aktif (Menu, Play, Score) akan mengambil alih kendali.