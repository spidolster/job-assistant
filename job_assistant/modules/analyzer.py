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
