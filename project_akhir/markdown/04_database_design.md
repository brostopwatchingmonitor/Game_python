# Rancangan 4: Skema Database (JSON)

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