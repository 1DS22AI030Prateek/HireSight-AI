import google.generativeai as genai

# Configure your Gemini API key
genai.configure(api_key="AIzaSyCLpNVsM1mFcYbHciagz5xtkWAS4XqBSs0")  # Replace with actual key or use os.getenv("GEMINI_API_KEY") if using env var

def get_resume_feedback(resume_text, jd_text):
    try:
        model = genai.GenerativeModel("models/gemini-1.5-pro")

        prompt = f"""
You are an expert resume coach and job market consultant.

Evaluate the following candidate resume against the provided job description.

Return:
- 3 to 5 specific and actionable suggestions.
- Format suggestions using bullet points (•).
- Focus on resume structure, missing skills, clarity, and alignment with JD.

Resume:
\"\"\"
{resume_text}
\"\"\"

Job Description:
\"\"\"
{jd_text}
\"\"\"
"""

        response = model.generate_content(prompt)
        return response.text.strip()

    except Exception as e:
        return f"⚠️ Unable to generate suggestion:\n\n{str(e)}"
