from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import config
from app.models import Base, Recruiter
from app.utils import hash_password

# Create database engine
engine = create_engine(config.DB_URL)

# Session factory for database access
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def init_db():
    """
    Create tables if not exists
    and insert default admin user
    """
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    if not db.query(Recruiter).first():
        admin = Recruiter(
            email="admin@ats.com",
            password_hash=hash_password("admin123")
        )
        db.add(admin)
        db.commit()
        print("✔ Default admin user created: admin@ats.com / admin123")
    db.close()
