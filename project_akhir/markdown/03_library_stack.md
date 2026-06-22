# Rancangan 3: Pilihan Library & Dependensi

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