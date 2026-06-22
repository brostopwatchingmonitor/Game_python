# Rancangan 6: Dokumentasi (Sphinx) & GitHub Wiki

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
    """
    Memvalidasi apakah pilihan pemain sesuai dengan kunci jawaban.

    Args:
        player_choice (int): Indeks jawaban yang diklik oleh pemain (0-3).
        correct_answer (int): Indeks kunci jawaban yang benar dari bank soal.

    Returns:
        bool: True jika jawaban benar, False jika salah.

    Raises:
        ValueError: Jika player_choice di luar rentang 0-3.
    """
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