"""Smoke-test helper for company/role extraction from raw JD text.

Usage:
    python test_extract.py

Requires:
    DEEPSEEK_API_KEY set in environment or .env.
"""
import os
import sys

# Add project package path so local modules are importable
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "job_assistant"))

from modules.analyzer import extract_company_and_role


def main() -> None:
    jd_text = (
        "Perusahaan: GoTo Gojek Tokopedia. "
        "Posisi: Senior Data Engineer. "
        "Requirement: Python, SQL, Airflow."
    )

    print("Testing extraction...")
    if not os.getenv("DEEPSEEK_API_KEY"):
        print("Warning: DEEPSEEK_API_KEY belum di-set. Hasil kemungkinan Unknown.")

    result = extract_company_and_role(jd_text)
    print("Result:")
    print(result)


if __name__ == "__main__":
    main()
