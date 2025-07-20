import streamlit as st
import os
import tempfile
import sys

# Allow imports from root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from scripts.jd_similarity import extract_text_from_pdf, calculate_similarity
from scripts.llm_suggester import get_resume_feedback

st.set_page_config(page_title="HireSight AI - Job Seeker", layout="wide")

# --- Custom Styles ---
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
        .evaluate-btn {
            background-color: #6A5ACD;
            color: white;
            font-size: 1.1rem;
            padding: 12px 30px;
            border-radius: 8px;
            border: none;
            cursor: pointer;
            transition: 0.3s ease;
            display: block;
            margin: 30px auto 10px;
        }
        .evaluate-btn:hover {
            background-color: #4B3FAE;
        }
        .match-box {
            background-color: #e6e0ff;
            border-left: 8px solid #6A5ACD;
            padding: 20px;
            margin-top: 20px;
            border-radius: 10px;
            font-size: 1.2rem;
            font-weight: bold;
            color: #333;
        }
        .ats-box {
            background-color: #e6f1ff;
            border-left: 8px solid #3a8ddc;
            padding: 20px;
            margin-top: 20px;
            border-radius: 10px;
            font-size: 1.1rem;
            font-weight: bold;
            color: #1a1a1a;
        }
        .suggest-box {
            background-color: #f7f5ff;
            padding: 15px;
            border-left: 5px solid #7e6dee;
            border-radius: 6px;
            margin-top: 20px;
            font-size: 0.96rem;
        }
    </style>
""", unsafe_allow_html=True)

# --- Back Button ---
st.markdown("""
    <a href="/" target="_self">
        <button class="back-btn">⬅️ Back to Home</button>
    </a>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("<h2 style='text-align: center; color:#4A3AFF;'>🎯 Resume Evaluator - Job Seeker Panel</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Upload your resume and job description to evaluate how well they match.</p>", unsafe_allow_html=True)

# --- Upload Inputs ---
resume_file = st.file_uploader("📄 Upload Your Resume (PDF)", type=["pdf"])

jd_input_type = st.radio("📝 How would you like to enter the Job Description?", ["Paste Text", "Upload File"])
jd_text = ""

if jd_input_type == "Paste Text":
    jd_text = st.text_area("✏️ Paste Job Description here", height=250)
else:
    jd_file = st.file_uploader("📎 Upload Job Description File (TXT)", type=["txt"])
    if jd_file is not None:
        jd_text = jd_file.read().decode("utf-8")
        st.info(f"📄 Loaded JD File: **{jd_file.name}**")

# --- Evaluate Button ---
evaluate_clicked = st.button("✨ Evaluate Match")

# --- Evaluation Logic ---
if evaluate_clicked:
    if resume_file and jd_text.strip():
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_resume:
            temp_resume.write(resume_file.read())
            resume_path = temp_resume.name

        try:
            resume_text = extract_text_from_pdf(resume_path)
            score = calculate_similarity(resume_text, jd_text)

            st.markdown(f"""
                <div class="match-box">
                    ✅ Match Score: {score}%<br>
                    {"🎉 Great match! You're likely a strong fit." if score >= 75 else "🟡 Decent match. Tailor your resume." if score >= 50 else "🔴 Low match. Improve resume content."}
                </div>
            """, unsafe_allow_html=True)

            # LLM Suggestion
            suggestion = get_resume_feedback(resume_text, jd_text)
            st.markdown(f"<div class='suggest-box'>{suggestion}</div>", unsafe_allow_html=True)

            # ATS Score
            def get_ats_score(text):
                score = 100
                if len(text) < 500: score -= 20
                if "email" not in text.lower(): score -= 15
                if "experience" not in text.lower(): score -= 10
                if text.count("\n") < 10: score -= 10
                return max(score, 0)

            ats_score = get_ats_score(resume_text)
            st.markdown(f"""
                <div class="ats-box">
                    📈 ATS Optimization Score: {ats_score}/100<br>
                    {"🟢 Strong ATS Compatibility" if ats_score >= 75 else "🟡 Moderate ATS Compatibility" if ats_score >= 50 else "🔴 Poor ATS Compatibility"}
                </div>
            """, unsafe_allow_html=True)

            # Skill Match
            def extract_skills(text):
                import re
                common_skills = ["python", "sql", "excel", "machine learning", "deep learning",
                                 "data analysis", "communication", "pandas", "numpy", "tensorflow",
                                 "powerbi", "azure", "aws", "cloud", "linux"]
                text = text.lower()
                return set(skill for skill in common_skills if re.search(r'\b' + re.escape(skill) + r'\b', text))

            jd_skills = extract_skills(jd_text)
            resume_skills = extract_skills(resume_text)

            missing_skills = jd_skills - resume_skills
            present_skills = resume_skills & jd_skills

            st.markdown("### 🧠 JD vs Resume Skills Match")
            st.markdown(f"""
                <div style='background-color:#e8fce8; border-left: 6px solid green;
                            padding: 12px 15px; border-radius: 6px; margin-top: 10px;'>
                    ✅ <b>Skills Found in Resume:</b> {", ".join(present_skills) if present_skills else 'None'}
                </div>
            """, unsafe_allow_html=True)
            st.markdown(f"""
                <div style='background-color:#fde8e8; border-left: 6px solid red;
                            padding: 12px 15px; border-radius: 6px; margin-top: 10px;'>
                    ❌ <b>Skills Missing:</b> {", ".join(missing_skills) if missing_skills else 'None'}
                </div>
            """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"⚠️ Error: {str(e)}")
        os.remove(resume_path)
    else:
        st.warning("⚠️ Please upload both resume and job description before evaluating.")
