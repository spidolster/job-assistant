import sys
import os

# Add to path so we can import modules
sys.path.append(os.path.join(os.path.dirname(__file__), "job_assistant"))

from modules.analyzer import extract_company_and_role

api_key = "AIzaSyDCvl6oKHt9IPs9JN6R0pGw96bbfGpTTeU"
jd_text = "Perusahaan: GoTo Gojek Tokopedia. Posisi: Senior Data Engineer. Requirement: Python, SQL, Airflow."

print("Testing extraction...")
result = extract_company_and_role(jd_text, api_key)
print("Result:")
print(result)
