from sqlalchemy import Column, String, Float, Text, TIMESTAMP, Boolean
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    job_title = Column(String, nullable=False)
    resume_text = Column(Text, nullable=False)
    resume_file_uri = Column(String, nullable=False)
    score = Column(Float, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())


class Recruiter(Base):
    __tablename__ = "recruiters"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
