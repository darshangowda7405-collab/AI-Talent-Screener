from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext

SECRET_KEY = "CHANGE_ME_IN_PRODUCTION"  # Replace later for real deployment!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password):
    """Hash a plain text password."""
    return pwd_context.hash(password)


def verify_password(password, hashed):
    """Verify a password against hashed version."""
    return pwd_context.verify(password, hashed)


def create_access_token(data: dict):
    """Create JWT token for secure session."""
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)algorithm=ALGORITHM)
