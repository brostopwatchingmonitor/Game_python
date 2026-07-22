# Void Mermaid: Hasumi and the Shattered Cores

Sebuah game platformer 2D aksi menggunakan bahasa pemrograman **Python** dan **Pygame Community Edition (pygame-ce)**. Project ini dibangun dengan arsitektur bersih (*Clean Code*), modular, serta menggunakan perhitungan fisika berbasis *Delta Time* dan sistem kamera clamping.

---

## 🎮 Kontrol Game

| Aksi | Tombol Keyboard / Mouse |
| :--- | :--- |
| **Bergerak Kiri / Kanan** | `A` / `D` atau `Panah Kiri` / `Panah Kanan` |
| **Melompat (Mendukung Double Jump)** | `Spasi` / `W` / `Panah Atas` |
| **Tebasan Pedang (3-Hit Combo)** | `Klik Kanan Mouse` |
| **Bertahan / Shield** | `Klik Kiri Mouse` (Tahan) |
| **Keluar Game** | `ESC` |

---

## 🛠️ Persyaratan Sistem (Prerequisites)

Pastikan komputer Anda sudah terinstal:
*   **Python 3.10** ke atas (sangat direkomendasikan).
*   Pip (Python Package Installer).

---

## 🚀 Panduan Instalasi dan Menjalankan Game

Ikuti langkah-langkah di bawah ini untuk menginstal dependensi dan menjalankan game dengan bersih:

### Langkah 1: Clone atau Download Source Code
Download repositori ini sebagai file ZIP lalu ekstrak, atau jalankan perintah git berikut jika Anda menggunakan Git:
```bash
git clone <url-repositori-ini>
cd project_akhir_pbo
```

### Langkah 2: Membuat Virtual Environment (Direkomendasikan)
Gunakan virtual environment agar instalasi pustaka game bersih dari package global sistem Anda:
*   **Windows:**
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```
*   **Linux / macOS:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

### Langkah 3: Menginstal Dependensi Game
Instal modul utama game, yaitu `pygame-ce` (bukan pygame biasa) dan `pytmx` untuk membaca format peta dari Tiled:
```bash
pip install pygame-ce pytmx
```

### Langkah 4: Menjalankan Game
Jalankan file entry-point utama yang berada di dalam folder `src/`:
```bash
python src/main.py
```

---

## 📁 Struktur Kode Program
*   `src/main.py` — Entry point utama untuk memulai game.
*   `src/game.py` — Pengatur loop utama game, inisialisasi Pygame, render kanvas, dan alur perulangan.
*   `src/player.py` — Logika input pemain, pergerakan berbasis Vector2, deteksi tabrakan presisi sumbu X/Y terpisah, serta animasi combo serangan dan pertahanan.
*   `src/sprites.py` — Kelas sprite ubin (Tilemap) untuk memuat dekorasi dan lantai solid.
*   `src/groups.py` — Kelas kustom `CameraGroup` yang melacak pemain dan membatasi scrolling kamera agar tidak melebihi tepi peta.
*   `src/settings.py` — Pengaturan dimensi layar, resolusi rendering, FPS, dan path aset game.
