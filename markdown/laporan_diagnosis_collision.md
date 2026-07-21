# Laporan Diagnosis Visual Karakter & Koordinat Tabrakan

Laporan ini menyajikan hasil diagnosis teknis terkait keluhan karakter yang terlihat tidak menapak secara visual di atas permukaan ubin tanah (*ground*).

---

## 1. Hasil Diagnosis Koordinat Fisik (Hitbox)
Kami menjalankan skrip simulasi physics di dalam mesin game untuk memantau koordinat aktual saat karakter mendarat di tanah. Berikut adalah data koordinat yang tercatat:

*   **Hitbox Karakter**: `<rect(38, 640, 40, 80)>`
    *   Sisi bawah (*bottom*) koordinat fisik pemain berada di koordinat **Y = 720** (yaitu `640 + 80`).
*   **Hitbox Ubin Tanah (Ground Tile)**: `<rect(0, 720, 48, 48)>`
    *   Sisi atas (*top*) koordinat fisik ubin tanah berada di koordinat **Y = 720**.
*   **Status Persinggungan**: `Is player bottom touching tile top? True`

> [!NOTE]
> **Kesimpulan Fisik**: Secara sistem fisika dan matematika Pygame, **hitbox karakter menempel sempurna pada batas atas ubin tanah (keduanya bertemu presisi di Y = 720)**. Tidak ada celah kosong atau bug pada sistem deteksi tabrakan (*collision logic*).

---

## 2. Penyebab Visual Karakter "Melayang" (Transparansi Aset)
Kami memeriksa susunan warna dan tingkat transparansi (*alpha channel*) pada ubin tanah asli di dalam berkas tileset **`Tiles.png`** (resolusi asli 16x16 piksel). Ditemukan data berikut:

*   **Baris 0 s.d 9**: Memiliki nilai **Alpha = 0** (100% transparan, kosong tanpa gambar).
*   **Baris 10 s.d 15**: Baru memiliki nilai **Alpha = 255** (gambar visual rumput dan tanah dimulai dari baris ke-11).

Saat ubin tersebut di-scale 3x lipat menjadi **48x48 piksel** di dalam game, area kosong transparan di bagian atas ubin melebar menjadi **30 piksel**.

```text
Visualisasi Ubin Tanah (48x48 Piksel):
┌──────────────────────────────┐  <- Batas atas Hitbox Fisik (Y = 720)
│                              │  
│  30 Piksel Kosong Transparan │  <- Kaki karakter berhenti di sini fisik
│                              │  
├──────────────────────────────┤  <- Batas atas Gambar Rumput (Y = 750)
│ ###### Gambar Rumput ####### │  
│ ###### Gambar Tanah ######### │  <- Sisi bawah Ubin Fisik (Y = 768)
└──────────────────────────────┘
```

Karena kaki karakter berdiri di batas fisik atas ubin (Y = 720), tetapi gambar rumput baru dimulai di Y = 750, karakter terlihat **melayang secara visual setinggi 30 piksel** di atas rumput.

---

## 3. Solusi yang Direkomendasikan

Kami menawarkan dua pendekatan untuk menyelaraskan visual ini:

### Opsi A: Kompensasi Offset Penggambaran Pemain (Sangat Direkomendasikan)
Kita cukup menggeser posisi penggambaran visual (*drawing offset*) pemain ke bawah sebesar **30 piksel** saat berpasangan dengan spritesheet 128x128.
*   **Implementasi**: Ubah nilai `self.image_offset.y` dari `-48` menjadi **`-18`** (yaitu `-48 + 30`).
*   **Keuntungan**: Sangat mudah diterapkan, hanya mengubah satu baris variabel di [player.py](file:///mnt/c/Users/ASUS/Documents/python/project_akhir_pbo/src/player.py). Tidak merusak sistem deteksi tabrakan horizontal, tebing, atau langit-langit yang sudah stabil.

### Opsi B: Pemotongan Tinggi Hitbox Ubin Tanah
Kita mengubah logika pemuatan peta di `game.py` untuk menggeser kotak tabrakan (`sprite.rect`) ubin tanah ke bawah sebesar 30 piksel.
*   **Kelemahan**: Kurang disarankan karena akan membuat hitbox ubin tanah tidak sejajar dengan ubin non-tabrakan/dekorasi lainnya di peta TMX, serta dapat menyebabkan musuh atau peluru terdeteksi menembus batas visual sebelum meledak.
