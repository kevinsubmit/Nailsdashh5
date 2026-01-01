"""
User database model
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from app.db.session import Base


class User(Base):
    """User model for FastAPI backend"""
    __tablename__ = "backend_users"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    username = Column(String(100), unique=True, nullable=False, index=True)
    full_name = Column(String(200), nullable=True)
    avatar_url = Column(String(500), nullable=True)
    phone = Column(String(20), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"
