from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from pathlib import Path
from fastapi import HTTPException
from typing import Optional
from pydantic import BaseModel
import os

JWT_SECRET= "ASODIHASD:AOIDH:AO()"
JWT_ALGORITHM = "HS256"

class SessionManager:
    """
    Manages user sessions
    """

    def __init__(self, secret_key: str, algorithm: str, upload_dir: Path, token_expiration_minutes: int = 60):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.upload_dir = upload_dir
        self.token_expiration_minutes = token_expiration_minutes

        self.upload_dir.mkdir(parents=True, exist_ok=True)

    def create_session(self) -> str:

        now = datetime.now(tz=timezone.utc)

        expiration = now + timedelta(minutes=self.token_expiration_minutes)

        payload = {
            "exp": expiration,
            "iat": now,
            "sub": str(os.urandom(16).hex()),
        }

        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

        session_path: Path = (self.upload_dir / payload["sub"])
        session_path.mkdir(parents=True, exist_ok=True)

        print(f"Session Path created is: {session_path}")

        return token
    
    def validate_session(self, token: str) -> str:

        try:
            print(f"TOKEN AGAIN {token}")
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            print(f"PAYLOAD {payload}")
            session_id = payload.get("sub")
            print("AFTER PAYLOAD SUB")
            if not session_id:
                raise HTTPException(status_code=400, detail="Invalid token payload")

            print("IT GOT HERE")
            self.get_session_path(session_id)

            return session_id
        
        except JWTError:
            print("THIS IS WHERE ERROR IS")
            raise HTTPException(status_code=401, detail="Invalid or expired token")
        
    
    def get_session_path(self, session_id: str) -> Path:

        session_path = self.upload_dir / session_id
        if not session_path.exists():
            raise HTTPException(status_code=404, detail="Session dir not found")

        print(f"Session Path is: {session_path}")
        return session_path
    
    def delete_session(self, session_id: str) -> None:

        session_path = self.upload_dir / session_id
        if session_path.exists():
            for file in session_path.iterdir():
                file.unlink()
            session_path.rmdir()