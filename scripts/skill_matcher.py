import spacy
from typing import List, Tuple

nlp = spacy.load("en_core_web_sm")

def extract_skill_candidates(text: str) -> List[str]:
    doc = nlp(text.lower())
    noun_phrases = set(chunk.text.strip() for chunk in doc.noun_chunks)
    keywords = set(token.text for token in doc if token.pos_ in ["NOUN", "PROPN"] and not token.is_stop)
    combined = noun_phrases.union(keywords)
    return [kw for kw in combined if len(kw) > 2 and not kw.isnumeric()]

def match_skills_from_jd(jd_text: str, resume_text: str) -> Tuple[List[str], List[str]]:
    jd_skills = extract_skill_candidates(jd_text)
    resume_skills = extract_skill_candidates(resume_text)
    matched = [skill for skill in jd_skills if skill in resume_skills]
    missing = [skill for skill in jd_skills if skill not in resume_skills]
    return matched, missing
