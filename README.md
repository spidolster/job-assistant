# 🕵️‍♂️ Job Assistant

**Job Assistant** adalah aplikasi sederhana berbasis Streamlit yang membantu kamu menganalisis kecocokan antara Resume (PDF) dan deskripsi pekerjaan (Job Description) secara cerdas menggunakan AI. Selain menilai kecocokan, aplikasi ini juga bisa mencatat (_track_) histori lamaran kamu secara otomatis!

## ✨ Fitur Utama
- Mengunggah Resume (PDF) dan otomatis mengekstrak teksnya.
- Menganalisis *Match Score*, kekuatan (*strengths*), kesenjangan (*gaps*), dan memberikan rekomendasi untuk posisi yang dilamar.
- Otomatis mengekstrak nama Perusahaan dan Posisi dari *raw text* lowongan menggunakan DeepSeek.
- Menyimpan histori lamaran dalam *Tracker* lokal agar rapih (menggunakan SQLite).

## 🛠️ Prasyarat
- **Python 3.9+** telah terinstal di komputer.
- Memiliki akun/API Key untuk setidaknya salah satu layanan AI (*DeepSeek*, *OpenAI*, *Gemini*, atau *Claude*).

## 🚀 Cara Menjalankan Aplikasi

1. **Clone repository ini (atau unduh folder project-nya).**
2. **Buka Terminal / Command Prompt**, arahkan ke folder utama project (`job_assistant`).
3. **Install semua dependencies** yang ada di `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```
4. **Siapkan API Key** (Sangat Disarankan):
   Duplikasi atau buat file bernama `.env` di direktori utama, lalu masukkan API keys yang kamu miliki:
   ```env
   OPENAI_API_KEY=sk-...
   DEEPSEEK_API_KEY=sk-...
   GEMINI_API_KEY=AIza...
   CLAUDE_API_KEY=sk-ant-...
   ```
   > *Catatan: Ekstraksi pintar Perusahaan & Posisi saat ini menggunakan DeepSeek, sehingga disarankan untuk mengisi `DEEPSEEK_API_KEY`.*
5. **Jalankan Aplikasi Streamlit**:
   ```bash
   python -m streamlit run job_assistant/app.py
   ```
6. **Mulai Analisis**:
   Buka browser di alamat `http://localhost:8501`. Unggah resume kamu, salin-tempel lowongan pekerjaan beserta nama perusahaannya, lalu klik "🚀 Analisis Kecocokan"!

## 📁 Struktur Folder Utama
- `job_assistant/app.py` — *Entry point* aplikasi antarmuka pengguna (Streamlit).
- `job_assistant/modules/` — Segala logika bisnis, *database*, *storage*, dan interaksi dengan *LLM*.
- `job_assistant/data/` — Direktori tempat menyimpan file resume `.pdf` dan *database* `.db` lokal kamu.
- `.env` — Konfigurasi _environment_ berisi kredensial rahasia (tidak masuk ke _version control/Git_).

## ⚖️ Lisensi
Project ini dibuat untuk kebutuhan personal. Gunakan sebijaknya!
