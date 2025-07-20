import streamlit as st

# Page config
st.set_page_config(page_title="HireSight AI", layout="wide")

# Custom CSS for updated style
st.markdown("""
    <style>
        .card {
            background-color: #ffffff;
            padding: 30px 25px;
            border-radius: 15px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
            margin-top: 40px;
        }
        .card h3 {
            color: #4A3AFF;
            font-size: 22px;
            margin-bottom: 10px;
            font-weight: 700;
        }
        .card p {
            font-size: 15px;
            color: #444;
        }
        .custom-btn {
            background-color: #ffffff;
            color: #4A3AFF;
            border: 2px solid #4A3AFF;
            padding: 10px 20px;
            border-radius: 8px;
            font-size: 15px;
            margin-top: 15px;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .custom-btn:hover {
            background-color: #4A3AFF;
            color: #ffffff;
        }
        [data-testid="stSidebar"] {
            background-color: #f0f2fb;
        }
        [data-testid="stSidebar"] .css-1v0mbdj {
            font-size: 1.15em;
            font-weight: 600;
            color: #372cae;
        }
    </style>
""", unsafe_allow_html=True)

# Title with new color
st.markdown("<h1 style='text-align: center; color: #4A3AFF;'>💼 HireSight AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 16px; color: #555;'>Intelligent Resume Evaluation & Candidate Ranking for Modern Hiring</p>", unsafe_allow_html=True)

# Layout: Side-by-side
col1, col2, _ = st.columns([1.2, 1.2, 0.6])

# Job Seeker block
with col1:
    st.markdown("""
        <div class="card">
            <h3>🎯 I'm a Job Seeker</h3>
            <p>
                Upload your resume and job description.<br>
                Get a match score, improvement tips, and shortlisting prediction.<br><br>
                <i>Powered by ML + LLM</i>
            </p>
            <a href="/User_Evaluator" target="_self">
                <button class="custom-btn">🔍 Evaluate My Resume</button>
            </a>
        </div>
    """, unsafe_allow_html=True)

# Recruiter block
with col2:
    st.markdown("""
        <div class="card">
            <h3>📘 I'm a Recruiter</h3>
            <p>
                Upload multiple resumes + job description.<br>
                Get ranked matches, missing skill tags, and exportable summaries.<br><br>
                <i>Ideal for hiring teams.</i>
            </p>
            <a href="/Recruiter_Ranker" target="_self">
                <button class="custom-btn">📊 Rank Candidates</button>
            </a>
        </div>
    """, unsafe_allow_html=True)

# Tip
st.markdown("<p style='text-align: center; font-size: 13px; margin-top: 30px;'>⚡ Tip: You can also use the sidebar to navigate between modules.</p>", unsafe_allow_html=True)
