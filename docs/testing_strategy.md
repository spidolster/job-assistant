# Testing Strategy (Discussion Draft)

Dokumen ini merangkum arah testing yang **simple, terpisah, dan scalable** untuk Job Assistant.

## Prinsip Utama
- Tujuan test: mencegah bug yang berdampak ke user.
- Test harus sederhana, cepat, dan mudah dirawat.
- Hindari test yang terlalu rapuh atau terlalu terikat detail implementasi.

## Struktur Folder (Terpisah dari App Code)
Semua test diletakkan terpusat di `tests/` dan **tidak** disebar ke folder modul aplikasi.

Contoh struktur saat project membesar:

- `tests/unit/` → test fungsi kecil/pure logic (parsing, helper)
- `tests/integration/` → test interaksi antar modul + SQLite
- `tests/e2e/` → test flow utama user (jumlah sedikit)
- `tests/fixtures/` → sample input/output statis

## Prioritas Test (Risk-based)
1. Parser kritikal: match score, salary range, ekstraksi field penting
2. Alur simpan data tracker/storage (termasuk duplicate handling)
3. Migrasi schema DB (forward-safe untuk data existing)
4. Routing provider/model (mock; tanpa panggil API live)

## Aturan Stabilitas
- Unit test wajib tanpa network call.
- Gunakan mock untuk LLM/provider.
- Integration test DB pakai temporary database.
- Test harus bisa dijalankan berulang dan independen urutan.

## Definition of Good Test (Praktis)
- Menangkap bug nyata yang pernah/berpotensi terjadi.
- Cepat dijalankan di local.
- Mudah dipahami dari nama test-nya.
- Jika gagal, penyebabnya jelas dan actionable.

## Hal yang Dihindari
- Test untuk hal yang terlalu sepele dan tidak memberi sinyal bug.
- Over-mocking sampai behavior nyata tidak teruji.
- Menambah test yang membuat maintenance berat tanpa nilai risiko yang jelas.
