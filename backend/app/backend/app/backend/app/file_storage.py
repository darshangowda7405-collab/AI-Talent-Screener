import os
import uuid
from app.config import config


class StorageManager:
    def save_resume(self, file_bytes: bytes, extension: str) -> str:
        """
        Save resume file locally but generate S3-style URI
        Example stored path: s3://ai-talent-screener-resumes/<id>.pdf
        """
        file_id = str(uuid.uuid4())
        cloud_uri = f"{config.STORAGE_BASE_URI}/{file_id}{extension}"

        # Local fallback for dev/demo
        local_dir = "backend/storage"
        os.makedirs(local_dir, exist_ok=True)
        local_path = os.path.join(local_dir, f"{file_id}{extension}")

        with open(local_path, "wb") as f:
            f.write(file_bytes)

        return cloud_uri


storage_manager = StorageManager()
