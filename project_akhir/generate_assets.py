import os
from PIL import Image, ImageDraw

def create_placeholder_assets():
    # Buat direktori yang dibutuhkan jika belum ada
    os.makedirs("assets/images", exist_ok=True)
    os.makedirs("assets/maps", exist_ok=True)
    os.makedirs("assets/sounds", exist_ok=True)

    # 1. Buat tilesheet gambar sederhana (64x64 piksel, terdiri dari 4x4 tiles berukuran 16x16)
    tilesheet_path = "assets/images/dungeon_tilesheet.png"
    if not os.path.exists(tilesheet_path):
        img = Image.new("RGBA", (64, 64), color=(0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Tile GID 1 (Lantai): Warna abu-abu terang dengan border sedikit gelap
        draw.rectangle([0, 0, 15, 15], fill=(80, 80, 80, 255), outline=(60, 60, 60, 255))
        
        # Tile GID 2 (Dinding): Warna abu-abu gelap dengan pola bata
        draw.rectangle([16, 0, 31, 15], fill=(40, 40, 40, 255), outline=(20, 20, 20, 255))
        draw.line([16, 8, 31, 8], fill=(60, 60, 60, 255))
        draw.line([24, 0, 24, 7], fill=(60, 60, 60, 255))
        draw.line([20, 8, 20, 15], fill=(60, 60, 60, 255))
        
        # Tile GID 3 (Lubang Pembuangan): Warna hitam dengan jeruji
        draw.rectangle([32, 0, 47, 15], fill=(20, 20, 20, 255), outline=(10, 10, 10, 255))
        draw.line([36, 0, 36, 15], fill=(100, 100, 100, 255))
        draw.line([40, 0, 40, 15], fill=(100, 100, 100, 255))
        draw.line([44, 0, 44, 15], fill=(100, 100, 100, 255))
        
        img.save(tilesheet_path)
        print(f"Asset dummy tilesheet berhasil dibuat: {tilesheet_path}")

if __name__ == "__main__":
    create_placeholder_assets()
