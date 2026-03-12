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
from modules.storage import save_resume, get_saved_resumes, get_resume_path, get_resume_text_from_db
from modules.document_utils import extract_text_from_uploaded_pdf, extract_text_from_pdf
from modules.analyzer import analyze_resume_vs_jd, extract_company_and_role
from modules.tracker import save_application, get_all_applications, delete_application

# Defined by user for auto-extraction
GEMINI_AUTO_EXTRACT_KEY = "AIzaSyDCvl6oKHt9IPs9JN6R0pGw96bbfGpTTeU"

# --- Init ---
init_db()
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

    resume_text = None
    uploaded_file = None

    if selected_resume_option == "📤 Upload Resume Baru":
        uploaded_file = st.file_uploader("Unggah file Resume (.pdf)", type=["pdf"])

        if uploaded_file:
            # Offer to save
            save_name = st.text_input(
                "Nama file untuk disimpan (opsional)",
                value=uploaded_file.name.replace(".pdf", ""),
                help="Kosongkan untuk nama otomatis dengan timestamp.",
            )
            if st.button("💾 Simpan Resume", key="save_resume"):
                saved_filename = save_resume(uploaded_file, custom_name=save_name)
                st.success(f"Resume disimpan sebagai: **{saved_filename}**")
                uploaded_file.seek(0)  # reset pointer after saving
                st.rerun()
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
    if st.button("🚀 Analisis Kecocokan", use_container_width=True, type="primary"):
        # Validate API Key
        api_key = get_api_key(selected_provider)
        if not api_key:
            st.error("❌ API Key belum diatur. Silakan masukkan API Key di sidebar.")
        elif not jd_text.strip():
            st.error("❌ Silakan masukkan Job Description terlebih dahulu.")
        else:
            resume_text = None
            resume_id = None
            
            # Extract/Retrieve resume text
            with st.spinner("Menyiapkan resume..."):
                if selected_resume_option == "📤 Upload Resume Baru":
                    if not uploaded_file:
                        st.error("❌ Silakan unggah resume terlebih dahulu.")
                        st.stop()
                    
                    # Auto-save the newly uploaded resume to history
                    with st.spinner("Menyimpan resume ke database..."):
                        save_result = save_resume(uploaded_file, custom_name="")
                        resume_id = save_result.get("id")
                        
                    # Still need to extract the text right now for the current analysis session
                    # because save_result doesn't return the text
                    resume_text = extract_text_from_uploaded_pdf(uploaded_file)
                else:
                    # Retrieve the text directly from the SQLite database
                    db_record = resume_map.get(selected_resume_option)
                    if db_record:
                        resume_id = db_record["id"]
                        resume_text = get_resume_text_from_db(resume_id)
                        
                        # Fallback text extraction just in case DB text is empty for some reason
                        if not resume_text:
                            resume_path = get_resume_path(selected_resume_option)
                            resume_text = extract_text_from_pdf(resume_path)

            if not resume_text:
                st.error("❌ Gagal membaca teks resume. Pastikan file tidak diproteksi atau berupa gambar.")
            else:
                # Analyze
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
                    
                    # Auto-extract company and role
                    with st.spinner("Mengekstrak info loker dengan Gemini..."):
                        extracted_info = extract_company_and_role(jd_text, GEMINI_AUTO_EXTRACT_KEY)
                        company_name = extracted_info.get("company", "Unknown Company")
                        role_name = extracted_info.get("role", "Unknown Role")
                    
                    # Save to tracker
                    if resume_id:
                        try:
                            save_application(
                                role=role_name,
                                company=company_name,
                                jd_text=jd_text,
                                resume_id=resume_id,
                                match_score=0, # Placeholder until we extract this reliably
                                analysis_result=analysis_result
                            )
                            st.info(f"💾 Disimpan ke Tracker: **{company_name} - {role_name}**")
                        except Exception as e:
                            st.error(f"Gagal menyimpan ke tracker: {e}")
                    
                    st.divider()
                    st.subheader("📊 Hasil Analisis")
                    st.markdown(analysis_result)

with tab_tracker:
    st.header("📊 Application Tracker")
    apps = get_all_applications()
    
    if not apps:
        st.info("Belum ada history lamaran. Mulai analisis di tab sebelah dan isi Nama Perusahaan & Posisi untuk menyimpannya ke Tracker.")
    else:
        import pandas as pd
        
        # Format for display
        display_data = []
        for a in apps:
            display_data.append({
                "ID": a["id"],
                "Tanggal": a["created_at"],
                "Perusahaan": a["company"],
                "Posisi": a["role"],
                "Resume Digunakan": a["resume_filename"] or "Terhapus/Unknown",
                "Skor": a["Match_score"] if a["Match_score"] else "-"
            })
            
        df = pd.DataFrame(display_data)
        
        # Make a nice dataframe
        st.dataframe(
            df,
            column_config={
                "ID": st.column_config.NumberColumn("ID", format="%d"),
                "Tanggal": st.column_config.DatetimeColumn("Tanggal", format="D MMM YYYY, HH:mm")
            },
            hide_index=True,
            use_container_width=True
        )

