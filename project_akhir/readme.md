# Dungeon Swordman: Queen Tesa - Game & Testing

Proyek ini telah dirapikan ke dalam struktur arsitektur modular yang memisahkan logika utama (*business/game logic*) dari antarmuka visual (*GUI/arcade render*). Pemisahan ini mempermudah proses pembuatan dan jalannya pengujian otomatis (*unit testing*) tanpa memerlukan inisialisasi window visual (OpenGL/arcade).

## Struktur Folder Project Baru

```text
project_akhir/
├── database/                   # File data game (.json)
│   └── balancing.json
├── core/                       # Logika dasar permainan (bebas dari library visual)
│   ├── __init__.py
│   ├── balancing.py            # Pengatur data balancing & fallback
│   ├── player.py               # Model status pemain & slot inventory
│   └── item_manager.py         # Logika magnet, item drop, & cooldowns
├── views/                      # Komponen visual / GUI menggunakan Arcade
│   ├── __init__.py
│   ├── menu_view.py
│   └── game_view.py
├── assets/                     # Multimedia resource (images, maps, sounds)
│   ├── images/
│   ├── maps/
│   └── sounds/
├── tests/                      # Unit testing untuk validasi logika core game
│   ├── __init__.py
│   ├── test_balancing.py
│   ├── test_player.py
│   └── test_item_manager.py
├── main.py                     # Entry point untuk menjalankan Game
├── generate_assets.py          # Script pembantu pembuat asset placeholder
├── requirements.txt            # Dependensi pustaka Python
└── readme.md                   # Panduan proyek
```

---

## 🚀 Cara Menjalankan Game

1. **Instal Dependensi:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Generate Asset Gambar Sederhana:**
   Sebelum memulai game untuk pertama kali, jalankan generator asset agar map dapat di-render:
   ```bash
   python3 generate_assets.py
   ```

3. **Mulai Game:**
   ```bash
   python3 main.py
   ```

---

## 🧪 Cara Menjalankan Unit Testing

Untuk memastikan semua sistem game berjalan normal (logika magnet item, drop/ambil item, slot inventory, dan balancing), Anda bisa menjalankan test suite menggunakan `pytest`:

1. **Jalankan semua pengujian secara otomatis:**
   ```bash
   python3 -m pytest
   ```

2. **Jalankan dengan output lebih detail (verbose):**
   ```bash
   python3 -m pytest -v
   ```