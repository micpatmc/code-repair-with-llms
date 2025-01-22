import uuid
from pathlib import Path
from typing import Dict

class SessionManager:
    """
    Manages user sessions and associated directories.
    """

    def __init__(self, upload_dir: Path):
        self.upload_dir = upload_dir
        self.sessions: Dict[str, Path] = {}

    def create_session(self) -> str:
        session_id = str(uuid.uuid4())
        session_path = self.upload_dir / session_id
        session_path.mkdir(parents=True, exist_ok=True)
        self.sessions[session_id] = session_path
        return session_id
    
    def get_sessions_path(self, session_id: str) -> Path:
        if session_id not in self.sessions:
            raise ValueError("Invalid session_id.")
        return self.sessions[session_id]
    
    def delete_session(self, session_id: str) -> None:
        if session_id in self.sessions:
            session_path = self.sessions.pop(session_id)

            for file in session_path.glob("*"):
                file.unlink()
            session_path.rmdir()