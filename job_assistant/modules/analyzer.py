"""
analyzer.py — Analyze a resume against a job description using an LLM.
Supports OpenAI and DeepSeek providers with configurable model selection.
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def analyze_resume_vs_jd(resume_text: str, jd_text: str, provider: str = "", model_name: str = "") -> str:
    """
    Analyzes a resume against a job description using an LLM.
    Args:
        resume_text: The extracted text from the user's resume.
        jd_text: The provided job description.
        provider: AI provider ('openai' or 'deepseek'). Falls back to env var.
        model_name: Specific model to use. Falls back to provider defaults.
    Returns:
        The analysis result including score, strengths, gaps, and recommendations.
    """
    if not provider:
        provider = os.getenv("AI_PROVIDER", "openai").lower()
    
    if provider == "openai":
        return _analyze_with_openai(resume_text, jd_text, model_name or "gpt-4o-mini")
    elif provider == "deepseek":
        return _analyze_with_deepseek(resume_text, jd_text, model_name or "deepseek-chat")
    elif provider == "gemini":
        return _analyze_with_gemini(resume_text, jd_text, model_name or "gemini-2.0-flash")
    elif provider == "claude":
        return _analyze_with_claude(resume_text, jd_text, model_name or "claude-3-7-sonnet-20250219")
    else:
        return f"Error: Unsupported AI provider '{provider}'"


def _analyze_with_openai(resume_text: str, jd_text: str, model_name: str) -> str:
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    prompt = _build_prompt(resume_text, jd_text)
    
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are an expert technical recruiter and career coach. Your output should be in Indonesian."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error during OpenAI API call: {e}"


def _analyze_with_deepseek(resume_text: str, jd_text: str, model_name: str) -> str:
    from openai import OpenAI
    client = OpenAI(
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com"
    )
    
    prompt = _build_prompt(resume_text, jd_text)
    
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are an expert technical recruiter and career coach. Your output should be in Indonesian."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error during DeepSeek API call: {e}"


def _analyze_with_gemini(resume_text: str, jd_text: str, model_name: str) -> str:
    """Use Google's OpenAI-compatible endpoint for Gemini models."""
    from openai import OpenAI
    client = OpenAI(
        api_key=os.getenv("GEMINI_API_KEY"),
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )

    prompt = _build_prompt(resume_text, jd_text)

    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are an expert technical recruiter and career coach. Your output should be in Indonesian."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error during Gemini API call: {e}"


def _analyze_with_claude(resume_text: str, jd_text: str, model_name: str) -> str:
    """Use the Anthropic SDK for Claude models."""
    import anthropic
    client = anthropic.Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))

    prompt = _build_prompt(resume_text, jd_text)

    try:
        response = client.messages.create(
            model=model_name,
            max_tokens=4096,
            system="You are an expert technical recruiter and career coach. Your output should be in Indonesian.",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return response.content[0].text
    except Exception as e:
        return f"Error during Claude API call: {e}"


def _build_prompt(resume_text: str, jd_text: str) -> str:
    return f"""
Tolong analisis resume berikut terhadap deskripsi pekerjaan (Job Description) yang diberikan.

--- JOB DESCRIPTION ---
{jd_text}

--- RESUME TEXT ---
{resume_text}

---
Buatlah analisis komprehensif dalam bahasa Indonesia dengan struktur berikut:
1. **Match Score**: Berikan estimasi persentase kecocokan (0-100%).
2. **Kekuatan (Strengths)**: Poin-poin di resume yang sangat cocok dengan kebutuhan JD.
3. **Kesenjangan (Gaps)**: Keterampilan atau pengalaman yang diminta di JD tapi tidak terlihat jelas di resume.
4. **Rekomendasi**: Saran spesifik untuk memperbaiki resume atau hal-hal yang perlu disiapkan untuk wawancara.
"""

def extract_company_and_role(raw_jd_text: str) -> dict:
    """
    Uses DeepSeek to extract the Company Name and Job Role from a raw text payload.
    Always uses DeepSeek (deepseek-chat) regardless of the provider selected in sidebar.
    Reads DEEPSEEK_API_KEY from environment / .env.
    Returns:
        dict: {"company": "Company Name", "role": "Job Role"}
    """
    from openai import OpenAI
    import json
    
    api_key = os.getenv("DEEPSEEK_API_KEY", "")
    if not api_key:
        print("DEEPSEEK_API_KEY not set, cannot extract company/role.")
        return {"company": "Unknown Company", "role": "Unknown Role"}
    
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com"
    )
    
    prompt = f"""
Given the following raw job description text, extract the Company Name and the Job Title (Role).
Return ONLY a valid JSON object with the keys "company" and "role".
Do not include any markdown formatting like ```json or anything else. Just the raw JSON string.
If you cannot find the company name, use "Unknown Company".
If you cannot find the job title, use "Unknown Role".

Raw Text:
{raw_jd_text}
"""
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.1  # Low temp for deterministic JSON extraction
        )
        
        result_text = response.choices[0].message.content.strip()
        
        # Clean up any potential markdown ticks that might have slipped through
        if result_text.startswith("```json"):
            result_text = result_text.replace("```json", "", 1)
        if result_text.endswith("```"):
            result_text = result_text[::-1].replace("```", "", 1)[::-1]
            
        result_text = result_text.strip()
        data = json.loads(result_text)
        
        return {
            "company": data.get("company", "Unknown Company"),
            "role": data.get("role", "Unknown Role")
        }
        
    except Exception as e:
        print(f"Extraction error: {e}")
        return {"company": "Unknown Company", "role": "Unknown Role"}

def extract_salary_range(jd_text: str) -> str:
    """
    Extract salary range information from raw job description text.
    Returns "-" when no clear salary signal is found.
    """
    import re

    if not jd_text:
        return "-"

    normalized = " ".join(jd_text.split())

    patterns = [
        r"(?i)(rp\.?\s?\d[\d\.,]*\s?(?:juta|jt|miliar|k|rb)?\s?(?:-|–|to|sampai)\s?rp\.?\s?\d[\d\.,]*\s?(?:juta|jt|miliar|k|rb)?(?:\s*/\s*(?:bulan|month|tahun|year))?)",
        r"(?i)((?:\d[\d\.,]*\s?(?:juta|jt|miliar|k|rb)\s?(?:-|–|to|sampai)\s?\d[\d\.,]*\s?(?:juta|jt|miliar|k|rb))\s*(?:/\s*(?:bulan|month|tahun|year))?)",
        r"(?i)(salary\s*(?:range)?\s*[:\-]?\s*rp\.?\s?\d[\d\.,]*\s?(?:-|–|to)\s?rp\.?\s?\d[\d\.,]*)",
        r"(?i)(gaji\s*(?:range)?\s*[:\-]?\s*rp\.?\s?\d[\d\.,]*\s?(?:-|–|to|sampai)\s?rp\.?\s?\d[\d\.,]*)",
    ]

    for pattern in patterns:
        match = re.search(pattern, normalized)
        if match:
            return match.group(1).strip()

    return "-"


def extract_match_score(analysis_text: str) -> int:
    """
    Extracts the match score percentage from the LLM analysis text using Regex.
    Defaults to 0 if not found.
    """
    import re
    if not analysis_text:
        return 0
        
    # Look for "Match Score" or similar context followed by a number and optionally a %
    match = re.search(r'(?i)match\s*score.*?(\d+)\s*%', analysis_text)
    if match:
        return int(match.group(1))
        
    match = re.search(r'(?i)kecocokan.*?(\d+)\s*%', analysis_text)
    if match:
        return int(match.group(1))
        
    match = re.search(r'(?i)score.*?:\s*(\d+)', analysis_text)
    if match:
        return int(match.group(1))
        
    # Fallback: find the first percentage in the text
    match = re.search(r'(\d+)\s*%', analysis_text)
    if match:
        return int(match.group(1))
        
    return 0


