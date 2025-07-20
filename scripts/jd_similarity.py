import os
import PyPDF2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text() or ''
    return text


def load_job_description(jd_path):
    with open(jd_path, 'r', encoding='utf-8') as file:
        return file.read()


def calculate_similarity(resume_text, jd_text):
    documents = [resume_text, jd_text]
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents)
    similarity_score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    return round(similarity_score[0][0] * 100, 2)  # Return as percentage


def get_resume_match_score(resume_path, jd_path):
    resume_text = extract_text_from_pdf(resume_path)
    jd_text = load_job_description(jd_path)

    if not resume_text.strip() or not jd_text.strip():
        return 0.0

    return calculate_similarity(resume_text, jd_text)


# Example run (you can comment this part out when importing elsewhere)
if __name__ == "__main__":
    resume = "data/resumes/prateek_resume.pdf"
    jd = "data/sample_jd.txt"
    score = get_resume_match_score(resume, jd)
    print(f"Match Score: {score}%")
