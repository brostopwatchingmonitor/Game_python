# Rancangan 1: Ikhtisar Proyek (Project Overview)

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