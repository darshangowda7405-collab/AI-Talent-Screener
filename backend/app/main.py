from fastapi import FastAPI, Form, UploadFile, File, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db import SessionLocal, init_db
from app.models import Candidate, Recruiter
from app.resume_parser import parse_resume
from app.file_storage import storage_manager
from app.ai_scoring import calculate_score
from app.utils import verify_password, create_access_token

init_db()
app = FastAPI(title="AI Talent Screener — Secure")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(Recruiter).filter_by(email=form.username).first()
    if not user or not verify_password(form.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/upload")
async def upload_resume(
    name: str = Form(...),
    email: str = Form(...),
    job_title: str = Form(...),
    job_description: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    file_bytes = await file.read()
    parsed = parse_resume(file_bytes, file.filename)
    result = calculate_score(parsed["text"], job_description)
    uri = storage_manager.save_resume(file_bytes, "." + file.filename.split(".")[-1])

    candidate = Candidate(
        name=name,
        email=email,
        job_title=job_title,
        resume_text=parsed["text"],
        resume_file_uri=uri,
        score=result["overall"]
    )

    db.add(candidate)
    db.commit()
    return {"id": candidate.id, "score": candidate.score}

@app.get("/ranked")
def ranked_candidates(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    return db.query(Candidate).order_by(Candidate.score.desc()).all()
