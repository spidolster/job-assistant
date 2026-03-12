import streamlit as st
import os
import sys

# Ensure local modules are importable
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.config import (
    load_config, save_api_key, get_api_key,
    save_provider, get_provider,
    save_model, get_model,
    AVAILABLE_MODELS,
)
from modules.db import init_db
from modules.storage import save_resume, get_saved_resumes, get_resume_path, get_resume_text_from_db, sync_resumes_from_disk
from modules.document_utils import extract_text_from_uploaded_pdf, extract_text_from_pdf
from modules.analyzer import (
    analyze_resume_vs_jd,
    extract_company_and_role,
    extract_match_score,
    extract_salary_range,
)
from modules.tracker import save_application, get_all_applications, delete_application

# --- Init ---
init_db()
sync_resumes_from_disk()  # Register any PDFs on disk not yet in SQLite
load_config()

st.set_page_config(page_title="Job Assistant", page_icon="🕵️", layout="wide")

st.title("🕵️‍♂️ Job Assistant")
st.markdown("Analisis kecocokan resume Anda dengan Job Description dan track history lamaran Anda.")

# ============================================================
# SIDEBAR — Settings
# ============================================================
with st.sidebar:
    st.header("⚙️ Pengaturan")

    # --- Provider ---
    providers = list(AVAILABLE_MODELS.keys())
    saved_provider = get_provider()
    default_idx = providers.index(saved_provider) if saved_provider in providers else 0
    selected_provider = st.selectbox("AI Provider", providers, index=default_idx, format_func=str.title)

    # Save provider choice
    if selected_provider != saved_provider:
        save_provider(selected_provider)

    # --- Model ---
    models = AVAILABLE_MODELS.get(selected_provider, [])
    saved_model = get_model()
    if saved_model in models:
        model_idx = models.index(saved_model)
    else:
        model_idx = 0
    selected_model = st.selectbox("Model LLM", models, index=model_idx)

    if selected_model != saved_model:
        save_model(selected_model)

    st.divider()

    # --- API Key ---
    st.subheader("🔑 API Key")
    current_key = get_api_key(selected_provider)
    masked_key = f"{'•' * 8}...{current_key[-4:]}" if len(current_key) > 4 else ""

    if masked_key:
        key_col, del_col = st.columns([3, 1])
        with key_col:
            st.success(f"Key tersimpan: {masked_key}")
        with del_col:
            if st.button("🗑️", key="del_key", help="Hapus API Key"):
                save_api_key(selected_provider, "")
                st.rerun()

    new_key = st.text_input(
        f"{selected_provider.title()} API Key",
        type="password",
        placeholder="Masukkan key baru untuk mengganti..." if current_key else "Masukkan API Key...",
    )

    if new_key and new_key != current_key:
        save_api_key(selected_provider, new_key)
        st.success("✅ API Key tersimpan!")
        st.rerun()

    if not current_key and not new_key:
        st.warning("⚠️ Belum ada API Key. Masukkan di atas untuk mulai analisis.")

# ============================================================
# MAIN — Tabs
# ============================================================
tab_analyze, tab_tracker = st.tabs(["🔍 Analyze & Apply", "📊 My Tracker"])

with tab_analyze:
    col1, col2 = st.columns(2)
    
    # --- Resume Input ---
    with col1:
        st.subheader("📄 Resume")
    
        saved_resumes = get_saved_resumes() # list of dicts: [{'id': 1, 'filename': '...'}]
        # Map filenames to IDs for easy lookup later
        resume_map = {r["filename"]: r for r in saved_resumes}
        
        resume_options = ["📤 Upload Resume Baru"] + list(resume_map.keys())
        selected_resume_option = st.selectbox("Pilih Resume", resume_options)

        uploaded_file = None
        if selected_resume_option == "📤 Upload Resume Baru":
            uploaded_file = st.file_uploader("Unggah file Resume (.pdf)", type=["pdf"])
            if uploaded_file:
                st.info(f"📎 File siap: **{uploaded_file.name}** — akan otomatis tersimpan saat Analisis.")
        else:
            # Using a saved resume
            resume_path = get_resume_path(selected_resume_option)
            if os.path.exists(resume_path):
                st.info(f"Menggunakan: **{selected_resume_option}**")
            else:
                st.error(f"File tidak ditemukan: {selected_resume_option}")

    # --- JD Input ---
    with col2:
        st.subheader("💼 Job Description (JD)")
        st.markdown("Paste *raw text* lowongan di sini (termasuk nama posisi dan perusahaan). Sistem akan memisahkannya otomatis lewat AI saat analisis.")
        jd_text = st.text_area("Teks Lengkap Job Description", height=300)
    
    # --- Analyze ---
    if st.button("🚀 Analisis Kecocokan", width="stretch", type="primary"):
        # Validate API Key
        api_key = get_api_key(selected_provider)
        if not api_key:
            st.error("❌ API Key belum diatur. Silakan masukkan API Key di sidebar.")
        elif not jd_text.strip():
            st.error("❌ Silakan masukkan Job Description terlebih dahulu.")
        else:
            resume_text = None
            resume_id = None
            
            # === Step 1: Prepare resume (text + ID) ===
            with st.spinner("Menyiapkan resume..."):
                if selected_resume_option == "📤 Upload Resume Baru":
                    if not uploaded_file:
                        st.error("❌ Silakan unggah resume terlebih dahulu.")
                        st.stop()
                    
                    # Extract text first (before save_resume moves the pointer)
                    uploaded_file.seek(0)
                    resume_text = extract_text_from_uploaded_pdf(uploaded_file)
                    
                    # Auto-save uploaded resume to DB + filesystem
                    uploaded_file.seek(0)
                    save_result = save_resume(uploaded_file, custom_name="")
                    resume_id = save_result.get("id")
                    
                    if resume_id:
                        st.success(f"📁 Resume disimpan: **{save_result.get('filename')}**")
                    else:
                        st.warning("⚠️ Gagal menyimpan resume ke database, tapi analisis tetap berjalan.")
                else:
                    # Retrieve from existing saved resume
                    db_record = resume_map.get(selected_resume_option)
                    if db_record:
                        resume_id = db_record["id"]
                        resume_text = get_resume_text_from_db(resume_id)
                        
                        # Fallback: extract from file if DB text is empty
                        if not resume_text:
                            resume_path = get_resume_path(selected_resume_option)
                            resume_text = extract_text_from_pdf(resume_path)

            if not resume_text:
                st.error("❌ Gagal membaca teks resume. Pastikan file tidak diproteksi atau berupa gambar.")
            else:
                # === Step 2: Analyze resume vs JD ===
                with st.spinner(f"Menganalisis dengan {selected_provider.title()} ({selected_model})..."):
                    analysis_result = analyze_resume_vs_jd(
                        resume_text, jd_text,
                        provider=selected_provider,
                        model_name=selected_model,
                    )
    
                # Check if the result is an error message from the API
                if analysis_result.startswith("Error"):
                    st.error(f"❌ {analysis_result}")
                    st.info("💡 Cek ulang API Key di sidebar. Pastikan key valid dan memiliki saldo/kredit.")
                else:
                    st.success("✅ Analisis Selesai!")
                    
                    # === Step 3: Auto-extract company & role (always DeepSeek) ===
                    with st.spinner("Mengekstrak info perusahaan & posisi dengan DeepSeek..."):
                        extracted_info = extract_company_and_role(jd_text)
                        company_name = extracted_info.get("company", "Unknown Company")
                        role_name = extracted_info.get("role", "Unknown Role")
                    st.info(f"🏢 **{company_name}** — 💼 **{role_name}**")
                    
                    # === Step 4: Save to tracker ===
                    try:
                        extracted_score = extract_match_score(analysis_result)
                        extracted_salary_range = extract_salary_range(jd_text)
                        save_application(
                            role=role_name,
                            company=company_name,
                            jd_text=jd_text,
                            resume_id=resume_id,  # Can be None if save failed, FK allows NULL
                            match_score=extracted_score,
                            salary_range=extracted_salary_range,
                            analysis_result=analysis_result,
                        )
                        st.info(
                            f"💾 Disimpan ke Tracker: **{company_name} — {role_name}** "
                            f"dengan skor **{extracted_score}%** dan salary range **{extracted_salary_range}**"
                        )
                    except Exception as e:
                        st.error(f"Gagal menyimpan ke tracker: {e}")
                    
                    st.divider()
                    st.subheader("📊 Hasil Analisis")
                    st.markdown(analysis_result)

with tab_tracker:
    st.header("📊 Application Tracker")
    apps = get_all_applications()
    
    if not apps:
        st.info("Belum ada history lamaran. Mulai analisis di tab sebelah untuk menyimpannya ke Tracker.")
    else:
        # Format for display
        display_data = []
        for a in apps:
            display_data.append({
                "ID": a["id"],
                "Tanggal": a["created_at"],
                "Perusahaan": a["company"],
                "Posisi": a["role"],
                "Resume Digunakan": a["resume_filename"] or "Terhapus/Unknown",
                "Skor": a["Match_score"] if a["Match_score"] else "-",
                "Salary Range": a["salary_range"] or "-"
            })
            
        # Make a nice dataframe directly from list of dicts (Supported by streamlit > 1.25)
        st.dataframe(
            display_data,
            column_config={
                "ID": st.column_config.NumberColumn("ID", format="%d"),
            },
            hide_index=True,
            use_container_width=True,
        )
