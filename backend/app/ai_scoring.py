from sentence_transformers import SentenceTransformer, util
from app.skill_extractor import extract_skills

model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

WEIGHTS = {
    "skills": 0.45,
    "experience": 0.30,
    "semantic": 0.25,
}


def extract_experience(text: str):
    import re
    # Extract patterns like "3 years", "2+ years"
    years = re.findall(r"(\\d+)\\+?\\s+years?", text.lower())
    if not years:
        return 0
    return max(int(y) for y in years)


def calculate_score(resume_text: str, job_desc: str):
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(job_desc)

    # Skill matching
    overlap = len(set(resume_skills) & set(jd_skills))
    skill_score = (overlap / max(len(jd_skills), 1)) * 100

    # Experience match
    exp_resume = extract_experience(resume_text)
    exp_required = extract_experience(job_desc)
    if exp_required > 0:
        exp_score = min((exp_resume / exp_required) * 100, 100)
    else:
        exp_score = 70  # Default if no experience mentioned
    exp_score = round(exp_score, 2)

    # Semantic similarity score
    emb_r = model.encode(resume_text, convert_to_tensor=True)
    emb_j = model.encode(job_desc, convert_to_tensor=True)
    semantic_score = util.cos_sim(emb_r, emb_j).item() * 100
    semantic_score = round(semantic_score, 2)

    # Weighted final score
    final_score = (
        skill_score * WEIGHTS["skills"] +
        exp_score * WEIGHTS["experience"] +
        semantic_score * WEIGHTS["semantic"]
    )
    final_score = round(final_score, 2)

    return {
        "overall": final_score,
        "skills_score": round(skill_score, 2),
        "experience_score": exp_score,
        "semantic_score": semantic_score,
        "resume_skills": resume_skills,
    }
