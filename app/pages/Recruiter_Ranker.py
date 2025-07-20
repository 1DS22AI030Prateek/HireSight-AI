import streamlit as st
import os
import tempfile
import sys
import pandas as pd
from datetime import datetime
import base64

# Allow imports from root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from scripts.jd_similarity import extract_text_from_pdf, calculate_similarity
from scripts.llm_suggester import get_resume_feedback

st.set_page_config(page_title="HireSight AI - Recruiter Panel", layout="wide")

# --------------------- Custom CSS ---------------------
st.markdown("""
    <style>
        .back-btn {
            background-color: #ffffff;
            border: 2px solid #4A3AFF;
            border-radius: 6px;
            padding: 8px 16px;
            font-size: 0.95em;
            color: #4A3AFF;
            cursor: pointer;
            transition: 0.3s;
            margin-bottom: 20px;
        }
        .back-btn:hover {
            background-color: #4A3AFF;
            color: #ffffff;
        }
        .summary-card {
            background-color: #f1f1fe;
            border-left: 6px solid #4A3AFF;
            border-radius: 10px;
            padding: 1.5rem;
            margin-bottom: 20px;
            box-shadow: 0 3px 6px rgba(0,0,0,0.1);
        }
        .download-button {
            background-color: #4A3AFF;
            color: white;
            padding: 14px 28px;
            font-size: 16px;
            font-weight: bold;
            border: none;
            border-radius: 8px;
            margin-top: 20px;
            cursor: pointer;
        }
        .rank-btn {
            background-color: #4A3AFF;
            color: white;
            font-size: 18px;
            font-weight: bold;
            border: none;
            padding: 14px 32px;
            border-radius: 10px;
            cursor: pointer;
        }
        .rank-btn:hover {
            background-color: #372cae;
        }
        .centered {
            display: flex;
            justify-content: center;
            margin-top: 25px;
            margin-bottom: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# --- Custom Button with Working Navigation ---
st.markdown("""
    <button class="back-btn" onclick="window.location.href='/';">⬅️ Back to Home</button>
""", unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center; color:#4A3AFF;'>📘 Recruiter Panel - Resume Ranker</h2>", unsafe_allow_html=True)

# --------------------- JD Input ---------------------
jd_text = ""
st.markdown("### 📝 Job Description")
jd_input_type = st.radio("Input JD", ["Paste Text", "Upload File"])
if jd_input_type == "Paste Text":
    jd_text = st.text_area("Paste the JD here:", height=200)
else:
    jd_file = st.file_uploader("Upload JD (.txt)", type=["txt"])
    if jd_file:
        jd_text = jd_file.read().decode("utf-8")
        st.success("✅ JD uploaded")

# --------------------- Resume Upload ---------------------
st.markdown("### 📂 Upload Resumes")
uploaded_resumes = st.file_uploader("Upload PDF Resumes", type=["pdf"], accept_multiple_files=True)

# --------------------- Skill Extraction ---------------------
def extract_skills(text):
    import re
    common_skills = ["python", "sql", "machine learning", "deep learning", "excel", "powerbi", "tensorflow", "communication", "pandas", "numpy", "scikit-learn", "aws", "cloud", "linux"]
    text = text.lower()
    return set(skill for skill in common_skills if re.search(r'\b' + re.escape(skill) + r'\b', text))

# --------------------- Init Session States ---------------------
if 'df_result' not in st.session_state:
    st.session_state.df_result = None
if 'view_mode' not in st.session_state:
    st.session_state.view_mode = "📋 Summary Cards"

# --------------------- Rank Button ---------------------
st.markdown("<div class='centered'>", unsafe_allow_html=True)
rank_clicked = st.button("📊 Rank Candidates", key="rank_btn", help="Click to process resumes", use_container_width=False)
st.markdown("</div>", unsafe_allow_html=True)

# --------------------- Processing ---------------------
if rank_clicked:
    if not jd_text.strip():
        st.warning("⚠️ Please enter or upload JD.")
    elif not uploaded_resumes:
        st.warning("⚠️ Please upload resumes.")
    else:
        scores = []
        jd_skills = extract_skills(jd_text)

        with st.spinner("⏳ Evaluating resumes..."):
            for resume in uploaded_resumes:
                try:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                        temp_file.write(resume.read())
                        temp_path = temp_file.name

                    resume_text = extract_text_from_pdf(temp_path)
                    score = calculate_similarity(resume_text, jd_text)
                    resume_skills = extract_skills(resume_text)
                    missing_skills = jd_skills - resume_skills
                    suggestion = get_resume_feedback(resume_text, jd_text)

                    scores.append({
                        "Candidate": resume.name,
                        "Match Score (%)": score,
                        "Missing Skills": ", ".join(missing_skills) if missing_skills else "None",
                        "LLM Suggestion": suggestion
                    })
                    os.remove(temp_path)
                except Exception as e:
                    st.error(f"❌ Error reading {resume.name}: {e}")

        if scores:
            df = pd.DataFrame(scores).sort_values(by="Match Score (%)", ascending=False).reset_index(drop=True)
            st.session_state.df_result = df
            st.success("✅ Ranking Complete")

# --------------------- Toggle View ---------------------
if st.session_state.df_result is not None:
    st.markdown("### 👁️ Switch View")
    st.session_state.view_mode = st.radio(
        "Choose how to view the results:",
        ["📋 Summary Cards", "📊 Ranking Table"],
        horizontal=True
    )

    df = st.session_state.df_result

    # --- Summary Cards View ---
    if st.session_state.view_mode == "📋 Summary Cards":
        for i, row in df.iterrows():
            st.markdown(f"""
                <div class="summary-card">
                    <h4>📄 <b>Candidate:</b> {row['Candidate']}</h4>
                    <ul>
                        <li><b>Match Score:</b> {row['Match Score (%)']}%</li>
                        <li><b>Missing Skills:</b> {row['Missing Skills']}</li>
                        <li><b>LLM Suggestions:</b></li>
                        <ul style="margin-left: 20px;">{row['LLM Suggestion']}</ul>
                    </ul>
                </div>
            """, unsafe_allow_html=True)

    # --- Table View ---
    elif st.session_state.view_mode == "📊 Ranking Table":
        st.markdown("### 📊 Candidate Ranking Table")
        st.dataframe(df[["Candidate", "Match Score (%)", "Missing Skills"]], use_container_width=True)

    # --- CSV Download ---
    csv = df.to_csv(index=False).encode("utf-8")
    b64 = base64.b64encode(csv).decode()
    filename = f"resume_ranking_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
    st.markdown(f"""
        <a href="data:file/csv;base64,{b64}" download="{filename}">
            <button class="download-button">📥 Download CSV Report</button>
        </a>
    """, unsafe_allow_html=True)
