```python
import os

files = {
    "01_project_overview.md": """# Rancangan 1: Ikhtisar Proyek (Project Overview)

## Deskripsi Game
**"MindMatrix: Trivia & Puzzle"** adalah game edukasi berbasis *desktop* yang menantang pengetahuan dan logika pemain. Game ini dirancang untuk menguji kecepatan berpikir melalui pertanyaan trivia pilihan ganda dan puzzle logika tebak angka/kata.

## Fitur Utama
1. **Sistem Kategori Soal**: Pemain dapat memilih antara "Trivia Pengetahuan" atau "Puzzle Logika".
2. **Sistem Timer Berbasis Frame**: Waktu menjawab dibatasi. Semakin cepat menjawab, bonus poin semakin besar.
3. **Papan Skor Lokal (Leaderboard)**: Menyimpan nama pemain dan skor tertinggi secara persisten.
4. **Sistem Nyawa (Lives)**: Pemain memiliki 3 nyawa. Salah menjawab akan mengurangi nyawa. Game over jika nyawa habis.

## Pembagian Tugas Tim (2-4 Orang)
Untuk mensimulasikan lingkungan kerja *software engineering* yang profesional, tugas dibagi menjadi peran spesifik. Setiap anggota wajib membuat *Standard Operating Procedure* (SOP) pengerjaan di *branch* masing-masing.

* **Project Lead & DevOps (Orang 1)**: 
    * Mengatur repositori GitHub, me-review *Pull Request* (PR).
    * Menyusun arsitektur *state machine* utama (Game Loop).
    * *Deliverable*: `main.py`, konfigurasi Git, *routing logic*.
* **UI/UX Programmer (Orang 2)**:
    * Membangun antarmuka menggunakan Pygame (menggambar *button*, teks, *background*).
    * Mengatur transisi layar (animasi transisi sederhana).
    * *Deliverable*: Semua file di *folder* `ui/`.
* **Core Logic & Engine (Orang 3)**:
    * Membuat sistem validasi jawaban, kalkulasi skor, dan timer.
    * Memastikan logika game murni tanpa terikat elemen visual (mudah di-test).
    * *Deliverable*: Modul di *folder* `core/`.
* **Database & Content (Orang 4)**:
    * Merancang skema JSON.
    * Menulis fungsi CRUD (*Create, Read, Update, Delete*) untuk interaksi file JSON.
    * *Data Entry* soal-soal trivia dan puzzle.
    * *Deliverable*: Modul `database/` dan file `.json`.
""",

    "02_folder_structure.md": """# Rancangan 2: Struktur Folder & Routing Logic

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
""",

    "03_library_stack.md": """# Rancangan 3: Pilihan Library & Dependensi

Proyek ini dibangun dengan mempertimbangkan dukungan jangka panjang dan kompatibilitas sistem operasi (*cross-platform*), termasuk kapabilitas berjalan mulus di lingkungan Linux/WSL maupun Windows.

## Stack Utama (`requirements.txt`)

| Library | Versi (Min) | Deskripsi & Alasan Penggunaan |
| --- | --- | --- |
| `pygame-ce` | `>=2.4.0` | **Community Edition Pygame.** Memiliki performa yang jauh lebih baik, perbaikan *bug* yang lebih cepat, dan dukungan *rendering* yang lebih modern dibandingkan Pygame standar. Berfungsi sebagai *engine* utama grafis, *event handling*, dan *audio*. |
| `pytest` | `>=8.0.0` | Framework untuk *unit testing*. Jauh lebih *clean* dan *pythonic* daripada `unittest` bawaan. Digunakan untuk memastikan logika *scoring* dan validasi struktur *database* tidak cacat. |
| `pydantic` | `>=2.5.0` | Sangat krusial untuk proyek berbasis JSON. Memvalidasi data JSON ke dalam objek Python dengan *type-checking* ketat, mencegah aplikasi *crash* akibat struktur file JSON yang diubah manual oleh pengguna. |
| `sphinx` | `>=7.2.0` | Generator dokumentasi standar industri untuk Python. Dipilih karena integrasinya yang kuat dengan repositori untuk membangun wiki teknis yang rapi. |
| `sphinx-rtd-theme` | `>=2.0.0` | Tema standar ReadTheDocs agar tampilan dokumentasi lebih profesional dan mudah dibaca (opsional namun sangat disarankan). |

## Standard Library (Bawaan Python)

* `json`: Modul standar untuk parsing *database* lokal (tidak perlu instal).
* `os` & `sys`: Untuk manajemen *path* agar *resource* (`assets/`) tetap bisa diakses terlepas dari OS (Windows, distro Linux, atau via WSL).
* `random`: Untuk mengacak kemunculan soal dari *database*.

> **Catatan Lingkungan WSL:** Jika ada anggota tim yang menjalankan Python menggunakan Windows Subsystem for Linux (WSL), pastikan WSLg (WSL GUI) sudah aktif agar *window* Pygame dapat dirender ke layar Windows.
""",

    "04_database_design.md": """# Rancangan 4: Skema Database (JSON)

Penyimpanan data memanfaatkan format JSON karena tidak membutuhkan instalasi server SQL. Menggunakan prinsip *Data Access Object* (DAO) agar pembacaan JSON efisien dan aman dari kerusakan korupsi data (*race condition* saat timpa-menimpa data).

## 1. Skema Bank Soal (`data/questions.json`)

Struktur data untuk Trivia dan Puzzle. Pydantic akan memvalidasi *key* ini saat game dijalankan.

```json
{
  "trivia": [
    {
      "q_id": "T001",
      "question": "Di antara bahasa berikut, mana yang sepenuhnya berbasis Object-Oriented?",
      "options": ["C", "Assembly", "Java", "HTML"],
      "correct_index": 2,
      "difficulty": 1
    }
  ],
  "puzzle": [
    {
      "q_id": "P001",
      "question": "Jika X = 5 dan Y = 10, maka X AND Y dalam gerbang logika Boolean menghasilkan?",
      "options": ["True", "False", "Error", "15"],
      "correct_index": 1,
      "difficulty": 3
    }
  ]
}
```

*Catatan: Menggunakan `correct_index` (integer) alih-alih teks jawaban langsung untuk memudahkan *shuffling* (pengacakan) posisi opsi di UI Pygame.*

## 2. Skema Leaderboard (`data/leaderboard.json`)

Menyimpan metrik pemain untuk kompetisi nilai akhir.

```json
[
  {
    "player_name": "Alif",
    "score": 1450,
    "questions_answered": 10,
    "accuracy_percentage": 85.5,
    "timestamp": "2026-06-17T20:30:00"
  },
  {
    "player_name": "Mahasiswa2",
    "score": 900,
    "questions_answered": 8,
    "accuracy_percentage": 60.0,
    "timestamp": "2026-06-16T10:15:20"
  }
]
```

## Mekanisme Data Access Object (DAO)

```python
# src/database/json_manager.py
import json
import os

class DatabaseManager:
    def __init__(self, filepath):
        self.filepath = filepath

    def fetch_all(self):
        if not os.path.exists(self.filepath):
            return []
        with open(self.filepath, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save_score(self, new_record):
        data = self.fetch_all()
        data.append(new_record)
        # Sort desc berdasarkan skor
        data.sort(key=lambda x: x['score'], reverse=True) 
        # Simpan top 10 saja untuk menghemat I/O file
        data = data[:10] 
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
```
""",

    "05_ui_design.md": """# Rancangan 5: Desain UI (Pygame Screens)

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
""",

    "06_documentation_guide.md": """# Rancangan 6: Dokumentasi (Sphinx) & GitHub Wiki

Menjaga dokumentasi yang baik adalah kunci kolaborasi tim yang sukses di perkuliahan dan dunia kerja.

## 1. Setup Sphinx (Documentation Generator)

Sphinx akan membaca komentar (*docstring*) di dalam kode Python kalian dan mengubahnya menjadi halaman *website* statis bergaya profesional.

**Langkah Inisialisasi:**

1. Jalankan `pip install sphinx sphinx-rtd-theme`
2. Di folder root proyek, jalankan `sphinx-quickstart docs`
3. Konfigurasi `docs/conf.py`:
```python
import os
import sys
sys.path.insert(0, os.path.abspath('../src')) # Agar Sphinx bisa membaca folder src

extensions = [
    'sphinx.ext.autodoc',     # Mengambil docstring otomatis
    'sphinx.ext.napoleon',    # Membaca format Google/NumPy style
    'sphinx.ext.viewcode'     # Menambahkan link ke source code
]
html_theme = 'sphinx_rtd_theme'
```

## 2. Standar Docstring (Google Style)

Semua fungsi utama di *folder* `src/` harus menggunakan format ini agar `napoleon` dapat merendernya dengan rapi:

```python
def check_answer(player_choice: int, correct_answer: int) -> bool:
    \"\"\"
    Memvalidasi apakah pilihan pemain sesuai dengan kunci jawaban.

    Args:
        player_choice (int): Indeks jawaban yang diklik oleh pemain (0-3).
        correct_answer (int): Indeks kunci jawaban yang benar dari bank soal.

    Returns:
        bool: True jika jawaban benar, False jika salah.

    Raises:
        ValueError: Jika player_choice di luar rentang 0-3.
    \"\"\"
    if not (0 <= player_choice <= 3):
        raise ValueError("Pilihan di luar rentang yang valid.")
    return player_choice == correct_answer
```

## 3. GitHub Wiki & Readme

Selain Sphinx untuk dokumentasi *source code* (API), file Markdown ini (`.md`) bisa langsung di-*copy-paste* ke tab **Wiki** di repositori GitHub kalian.

* **README.md** di root folder wajib berisi:
1. Cara instalasi (`pip install -r requirements.txt`).
2. Cara menjalankan game (`python src/main.py`).
3. Screenshot *gameplay* (menambah nilai estetika saat dosen mereview repositori).
""",

    "07_git_workflow_and_setup.md": """# Rancangan Tambahan: Standar Git & File .gitignore

File ini sangat vital untuk mencegah konflik kodingan antar anggota kelompok dan menjaga repositori tetap bersih dari file sampah lokal.

## 1. Konfigurasi Wajib: `.gitignore`

Simpan file ini di *root directory* dengan nama `.gitignore` (tanpa ekstensi apa pun). Ini mencegah file *cache* Python dan log database ter-*upload* ke GitHub.

```text
# Python cache & virtual environment
__pycache__/
*.py[cod]
*$py.class
venv/
env/
.env

# Pytest
.pytest_cache/

# Database log (Sangat penting agar tidak bentrok antar anggota)
data/leaderboard.json

# OS generated files
.DS_Store
Thumbs.db
```

*(Catatan: `leaderboard.json` di-*ignore* karena akan digenerate secara lokal oleh `DatabaseManager` ketika aplikasi dijalankan. File statis seperti `questions.json` **TIDAK** di-*ignore* agar soal bisa dipakai semua anggota).*

## 2. SOP Alur Kolaborasi GitHub (Feature Branching)

Jangan pernah melakukan koding langsung di branch `main`.

1. **Sinkronisasi Awal (Setiap mau ngoding)**
```bash
git checkout main
git pull origin main
```

2. **Membuat Branch Tugas (Contoh: Bikin fitur skor)**
```bash
git checkout -b feature/hitung-skor
```

3. **Mengerjakan Tugas & Simpan Perubahan**
```bash
git add .
git commit -m "feat: menambah kalkulasi logika skor berdasarkan timer"
git push origin feature/hitung-skor
```

4. **Pull Request (PR)**
Buka GitHub, buat *Pull Request* dari branch `feature/hitung-skor` ke `main`. Minta anggota lain mengecek kode kalian sebelum menekan tombol *Merge*.
"""
}

generated_files = []
for filename, content in files.items():
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content.strip())
    generated_files.append(filename)

print("Files generated:", generated_files)
```

Semua file rancangan Markdown yang kamu minta sudah selesai dibuat. Sebagai tambahan yang krusial untuk kesuksesan proyek tim kamu, saya juga membuatkan file ke-7 (`07_git_workflow_and_setup.md`) yang berisi *Standard Operating Procedure* (SOP) repositori dan *template* `.gitignore`.

File ini sangat penting mengingat pengembangan proyek di dalam tim membutuhkan aturan kolaborasi yang kuat (*branching*), serta untuk memastikan konfigurasi *virtual environment* lokal atau sistem operasi tidak ikut masuk dan menyebabkan konflik kode di GitHub.

Berikut adalah 7 file yang sudah siap kamu unduh dan bagikan ke tim proyekmu:

[file-tag: code-generated-file-6-1781712974851613552]
[file-tag: code-generated-file-5-1781712974851612882]
[file-tag: code-generated-file-4-1781712974851612002]
[file-tag: code-generated-file-3-1781712974851611492]
[file-tag: code-generated-file-2-1781712974851610782]
[file-tag: code-generated-file-1-1781712974851609982]
[file-tag: code-generated-file-0-1781712974851606002]

Jika tim kamu melakukan pengembangan *game* menggunakan *environment* Linux (seperti WSL), pastikan konfigurasi tampilan GUI-nya (seperti WSLg) sudah diaktifkan agar jendela UI Pygame dapat muncul dan dirender dengan baik di layar komputer saat kalian melakukan demonstrasi proyek. Selamat mengerjakan *game*-nya!