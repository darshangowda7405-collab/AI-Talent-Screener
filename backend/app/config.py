import os

class Config:
    # Cloud-ready file storage path (local fallback)
    STORAGE_BUCKET = os.getenv("STORAGE_BUCKET", "ai-talent-screener-resumes")
    STORAGE_BASE_URI = f"s3://{STORAGE_BUCKET}"

    # PostgreSQL database config (Docker)
    DB_URL = os.getenv(
        "DB_URL",
        "postgresql://postgres:password@db:5432/ats_db"
    )

config = Config()
