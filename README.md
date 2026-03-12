# 🕵️‍♂️ Job Assistant

**Job Assistant** adalah aplikasi yang membantu kamu menganalisis kecocokan antara Resume (PDF) dan deskripsi pekerjaan (Job Description) secara cerdas menggunakan AI. Selain menilai kecocokan, aplikasi ini juga mencatat (_track_) histori lamaran secara otomatis.

## ✨ Fitur Utama
- Upload Resume (PDF) dan otomatis mengekstrak teksnya.
- **Match Score** + analisis kekuatan, kesenjangan, dan rekomendasi.
- Otomatis mengekstrak nama Perusahaan dan Posisi dari raw text lowongan (DeepSeek).
- **Application Tracker** — histori lamaran tersimpan di SQLite lokal.
- Multi-provider AI: **OpenAI**, **DeepSeek**, **Gemini**, **Claude**.
- **Dua mode UI**: Streamlit monolith (Phase 2) dan React + FastAPI (Phase 3).

## 🛠️ Prasyarat
- **Python 3.9+**
- **Node.js 18+** (untuk frontend React)
- API Key untuk minimal 1 provider AI (DeepSeek, OpenAI, Gemini, atau Claude)

## 🚀 Cara Menjalankan

### Opsi A: Streamlit (Monolith)
```bash
pip install -r requirements.txt
python -m streamlit run job_assistant/app.py
```
Buka `http://localhost:8501`.

### Opsi B: FastAPI + React (Phase 3)
```bash
# Terminal 1 — Backend
pip install -r requirements.txt
python -m uvicorn job_assistant.backend.main:app --port 8000

# Terminal 2 — Frontend
cd frontend
npm install
npm run dev
```
Buka `http://localhost:5173`. Frontend akan memanggil backend di `http://localhost:8000`.

Override backend URL jika perlu:
```bash
VITE_API_BASE=http://host-lain:8000
```

### Konfigurasi API Key
Buat file `.env` di root project:
```env
OPENAI_API_KEY=sk-...
DEEPSEEK_API_KEY=sk-...
GEMINI_API_KEY=AIza...
CLAUDE_API_KEY=sk-ant-...
```
> *Ekstraksi otomatis Perusahaan & Posisi menggunakan DeepSeek, jadi `DEEPSEEK_API_KEY` sangat disarankan.*

## 🧪 Testing

### Unit & Integration Tests
```bash
python -m unittest discover -s tests -v
```
Saat ini: **19 tests** (unit + integration) mencakup:
- Parser score/salary (10 test cases)
- API endpoint: health, analyze, upload validation
- Tracker/storage integration (SQLite temp DB)
- File upload validation (size limit 5MB, PDF magic bytes)
- Delete non-existent tracker entry

### Browser Automated Tests
Jalankan backend + frontend, lalu gunakan browser test untuk verifikasi:
- Page load & structure (title, sections, labels)
- Form interactions (dropdown switching, button enable/disable)
- Tracker table rendering

## 🔒 Security
- **CORS**: Default `http://localhost:5173` (bukan wildcard `*`). Override via env `CORS_ALLOW_ORIGINS`.
- **Upload validation**: Maks 5MB + validasi PDF magic bytes (`%PDF`).
- **Input limit**: JD text maks 50.000 karakter.
- **Error sanitization**: Error messages tidak mengandung API key atau data sensitif.
- **Parameterized SQL**: Semua query menggunakan placeholder `?` (bukan string format).

## 📁 Struktur Folder
```
job_assistant/
├── app.py                  # Entry point Streamlit (Phase 2)
├── backend/
│   ├── main.py             # FastAPI entry point (Phase 3)
│   └── schemas.py          # Pydantic request/response models
├── modules/
│   ├── analyzer.py         # LLM analysis + score/salary extraction
│   ├── config.py           # API key management (.env)
│   ├── db.py               # SQLite schema + migrations
│   ├── document_utils.py   # PDF text extraction
│   ├── storage.py          # Resume file + DB management
│   └── tracker.py          # Application tracking CRUD
├── data/
│   ├── resumes/            # Uploaded resume PDFs
│   └── job_assistant.db    # SQLite database
frontend/
├── src/App.jsx             # React UI
├── package.json
tests/
├── unit/                   # Parser & API unit tests
├── integration/            # Tracker/storage integration tests
docs/
├── qa_report.md            # QA test report
├── testing_strategy.md     # Testing guidelines
```

## ⚖️ Lisensi
Project ini dibuat untuk kebutuhan personal. Gunakan sebijaknya!
