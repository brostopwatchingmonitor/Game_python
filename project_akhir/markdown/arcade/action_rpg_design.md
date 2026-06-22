# Rencana Desain Game: Action RPG (Python Arcade)

Dokumen ini berisi rancangan arsitektur, mekanik, dan fitur untuk game Action RPG 2D yang dibangun menggunakan library **Python Arcade**.

---

## 1. Konsep Game & Ikhtisar (Game Concept & Overview)

*   **Genre**: Action Role-Playing Game (Action RPG) 2D Top-Down.
*   **Tema**: Dark Dungeon Adventure.
*   **Perspektif**: Top-Down (tampilan dari atas seperti RPG Maker / *Omori*).
*   **Gaya Visual**: Retro Low-Quality Pixel Art (seperti game *Super Mario Bros.* jadul).
*   **Library Utama**: `arcade` (Python), `pytiled_parser` (untuk memuat peta dari Tiled Map Editor).
*   **Target Gameplay**:
    *   Pemain mengendalikan seorang **Swordman (Ksatria Pedang)** menjelajahi dungeon gelap.
    *   Tujuan akhir game adalah mengalahkan **Queen Tesa**, penguasa dungeon tersebut.

---

## 2. Fitur Utama & Mekanik Game

### A. Kontrol Pemain & Pergerakan (Swordman)
*   **Pergerakan**: Tombol `W`, `A`, `S`, `D` atau tombol Panah untuk bergerak ke 4/8 arah.
*   **Serangan**: Tombol `Space` atau Klik Kiri Mouse untuk mengayunkan pedang (serangan jarak dekat / *melee*).
*   **Dodge Dash**: Tombol `Shift` untuk melakukan dorongan cepat (dash) menghindari serangan musuh. Berguna untuk merapatkan jarak dengan boss fase 1.

### B. Mekanik Pertempuran & Pencahayaan (Combat & Lighting)
*   **Hitbox & Collision**: Menggunakan `arcade.SpriteList` untuk mendeteksi tabrakan tebasan pedang dengan musuh.
*   **Sistem Pencahayaan (Shading Light/Aura)**:
    *   Karakter memiliki lingkaran cahaya (*light aura*) di sekelilingnya yang menerangi dungeon gelap.
    *   *AI Enemy Activation*: Musuh di luar area cahaya akan berada dalam kondisi tidur/pasif. Musuh hanya akan aktif mengejar pemain jika masuk ke dalam radius cahaya karakter utama (jarak deteksi AI sama dengan radius cahaya).
*   **Sistem HP**: Pemain memiliki sejumlah Health Points. Jika HP mencapai 0, game over.

### C. Sistem Inventory & Item Drop
*   **Slot UI Utama**: Inventory langsung tertera pada HUD utama (misal: 3–5 slot di bagian bawah layar).
*   **Loot & Auto-Pickup (Magnet Range)**:
    *   Peti kayu harus dihancurkan atau musuh dikalahkan untuk menjatuhkan (*drop*) item.
    *   Pemain memiliki **radius hisap (vacuum range)**. Jika pemain mendekati item dalam radius tersebut, item akan bergerak otomatis dan masuk ke inventory pemain jika masih ada slot kosong.
*   **Mekanisme Drop Manual (`Slot` + `Q`)**:
    *   Pemain menekan tombol angka (misal `1`, `2`, `3`) untuk memilih slot, lalu menekan tombol `Q` untuk menjatuhkan (*drop*) item tersebut kembali ke tanah.
    *   **Cooldown Jeda 5 Detik**: Item yang baru saja dijatuhkan secara manual akan memiliki jeda waktu 5 detik sebelum dapat ditarik kembali oleh radius auto-pickup pemain, mencegah terjadinya putaran ambil-jatuh terus-menerus.
*   **Item Khusus Portal**:
    *   Pemain wajib mencari dan mendapatkan item khusus (misal: *Emblem Queen Tesa* atau *Portal Key*) di dalam dungeon untuk dapat membuka portal yang menuju ke ruangan bos terakhir.

### D. Boss Fight: Queen Tesa
Pertarungan boss dibagi menjadi 2 fase yang menuntut keterampilan pemain dalam menggunakan mekanik karakter:
*   **Fase 1 (Ranged/Jarak Jauh)**: Queen Tesa menyerang dari jarak jauh menggunakan proyektil sihir menyebar. Pemain harus memanfaatkan *Dodge Dash* untuk menghindari peluru dan mendekatinya untuk menyerang.
*   **Fase 2 (Melee Brutal/Jarak Dekat)**: Setelah HP Boss mencapai batas tertentu (misal 50%), ia beralih ke serangan jarak dekat yang sangat brutal, cepat, dan agresif. Pemain harus cermat membaca animasi serangan dan menghindar pada waktu yang tepat.

### E. Penyelamatan Progres (Save/Load JSON)
*   Game menyimpan data progres ke dalam file `save_data.json`.
*   Data yang disimpan meliputi: Level Pemain, Koin/Gold, Item di Inventory, dan apakah Boss Queen Tesa sudah dikalahkan.

---

## 3. Arsitektur Kode & Struktur Folder

```text
project_akhir/
│
├── main.py                    # Entry point aplikasi & inisialisasi window
├── database/
│   ├── balancing.json         # Konfigurasi stats (HP, ATK, XP) untuk balancing
│   └── save_data.json         # File penyimpanan progres game
│
├── assets/                    # Resource game (low-quality pixel art)
│   ├── images/                # Karakter, musuh, tile, peti, UI
│   ├── sounds/                # Musik latar belakang & SFX tebasan/hancur
│   └── maps/                  # Dungeon map (.tmx)
│
├── core/                      # Logika murni game
│   ├── __init__.py
│   ├── player.py              # Kelas Player (Swordman, HP, Dash, Light Radius)
│   ├── enemy.py               # AI Musuh & Boss Queen Tesa (Fase 1 & Fase 2)
│   ├── inventory.py           # Manajemen Slot Quick Inventory & Auto-pickup
│   └── save_system.py         # Logika baca/tulis JSON save_data.json
│
└── views/                     # Pengatur Tampilan (State Machine / View)
    ├── __init__.py
    ├── loading_view.py        # Layar loading saat memuat map berat
    ├── menu_view.py           # View Main Menu
    ├── game_view.py           # View Arena Dungeon Utama
    └── game_over_view.py      # View Game Over / Kemenangan
```

---

## 4. Analisis Solusi Kritik & Evaluasi Potensi Masalah

### Solusi 1: Sistem Cahaya (Lighting System) untuk AI Activation
*   **Penerapan**: Sangat bisa diterapkan.
    *   *Teknik Ringan*: Dibandingkan menggunakan OpenGL Shader yang rumit dan berat, kita bisa menggunakan **tumpukan gambar hitam transparan (overlay)** dengan bagian tengah berlubang (transparan) di posisi pemain.
    *   *AI Trigger*: Deteksi jarak Euclidean sederhana antara `Player` dan `Enemy` dapat mewakili batas cahaya. Jika `Jarak < Radius Cahaya`, maka status AI musuh berubah menjadi `ACTIVE`. Ini sangat menghemat CPU karena musuh yang jauh tidak akan memproses AI.
*   **Kritik Solusi**: Jika musuh di luar cahaya tiba-tiba aktif sebelum terlihat di layar karena radius cahaya terlalu besar, hal ini dapat merusak efek kejutan dungeon. Radius cahaya harus disesuaikan dengan ukuran layar (`viewport`).

### Solusi 2: Layar Pemuatan (Loading Screen) untuk Mengatasi Lag
*   **Penerapan**: Ide bagus dan sangat realistis untuk tugas akhir semester 2.
    *   Menggunakan `arcade.View` khusus bernama `LoadingView` untuk memuat asset gambar dan mem-parsing peta Tiled `.tmx` sebelum masuk ke `GameView`.
*   **Kritik Solusi**: Untuk map yang sangat kecil, loading screen yang terlalu lama akan mengganggu kenyamanan bermain. Loading screen sebaiknya hanya muncul saat pertama kali game dijalankan atau saat berpindah lantai dungeon.

### Solusi 3: Penyimpanan Statistik di File Konfigurasi (Balancing Config)
*   **Rekomendasi Solusi**: Buat file `database/balancing.json` untuk menampung seluruh statistik dasar. Contoh struktur JSON:
    ```json
    {
      "player": {
        "max_hp": 100,
        "attack_power": 15,
        "speed": 4
      },
      "enemy_skeleton": {
        "hp": 30,
        "attack_power": 5,
        "speed": 2
      },
      "boss_queen_tesa": {
        "hp": 500,
        "attack_power": 25,
        "speed": 3
      }
    }
    ```
*   **Kritik Solusi**: Membaca file JSON berulang kali di dalam game loop akan menyebabkan lag. Data balancing ini harus dibaca **sekali saja** saat game dijalankan (*startup*) dan disimpan dalam variabel memori global atau kelas *Config Manager*.
