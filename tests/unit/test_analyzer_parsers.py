"""Unit tests for analyzer parser helpers (critical, deterministic paths)."""

import unittest

from job_assistant.modules.analyzer import extract_match_score, extract_salary_range


class TestExtractMatchScore(unittest.TestCase):
    """Verify score parsing from common LLM output variants."""

    def test_extract_match_score_standard_label(self) -> None:
        text = "Match Score: 82%\nKekuatan: ..."
        self.assertEqual(extract_match_score(text), 82)

    def test_extract_match_score_kecocokan_label(self) -> None:
        text = "Tingkat kecocokan kandidat sekitar 76% berdasarkan JD."
        self.assertEqual(extract_match_score(text), 76)

    def test_extract_match_score_numeric_without_percent_after_score_label(self) -> None:
        text = "Score: 91\nSummary: sangat relevan"
        self.assertEqual(extract_match_score(text), 91)

    def test_extract_match_score_fallback_first_percentage(self) -> None:
        text = "Relevansi pengalaman 68% dan skill coverage 70%."
        self.assertEqual(extract_match_score(text), 68)

    def test_extract_match_score_returns_zero_when_missing(self) -> None:
        text = "Tidak ada angka persentase atau score numerik di output."
        self.assertEqual(extract_match_score(text), 0)


class TestExtractSalaryRange(unittest.TestCase):
    """Verify salary range parsing from raw JD text patterns."""

    def test_extract_salary_range_with_rupiah_prefix(self) -> None:
        jd_text = "Kami menawarkan gaji Rp 8 juta - Rp 12 juta / bulan untuk posisi ini."
        self.assertEqual(extract_salary_range(jd_text), "Rp 8 juta - Rp 12 juta / bulan")

    def test_extract_salary_range_without_rupiah_prefix(self) -> None:
        jd_text = "Compensation: 10 juta sampai 15 juta / month + bonus kinerja"
        self.assertEqual(extract_salary_range(jd_text), "10 juta sampai 15 juta / month")

    def test_extract_salary_range_salary_label_pattern(self) -> None:
        jd_text = "Salary range: Rp12.000.000 to Rp18.000.000"
        self.assertEqual(extract_salary_range(jd_text), "Rp12.000.000 to Rp18.000.000")

    def test_extract_salary_range_returns_dash_when_missing(self) -> None:
        jd_text = "Benefit: laptop, asuransi kesehatan, cuti tahunan."
        self.assertEqual(extract_salary_range(jd_text), "-")

    def test_extract_salary_range_returns_dash_for_empty_input(self) -> None:
        self.assertEqual(extract_salary_range(""), "-")


if __name__ == "__main__":
    unittest.main()
