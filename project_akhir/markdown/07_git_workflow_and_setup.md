# Rancangan Tambahan: Standar Git & File .gitignore

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