import re

# Initial tech skills dictionary — easily expandable
SKILLS = {
    "python", "java", "c", "c++", "javascript", "typescript",
    "react", "angular", "node", "express", "sql",
    "mysql", "postgresql", "mongodb",
    "aws", "docker", "kubernetes",
    "html", "css", "linux", "git", "django", "flask", "fastapi"
}


def extract_skills(text: str):
    """
    Extracts known skills that appear in the text.
    """
    words = set(re.findall(r"[A-Za-z+#]+", text.lower()))
    matched = SKILLS & words
    return sorted(list(matched))
