"""
CRUD operations for User model
"""
from typing import Optional
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash


def get(db: Session, id: int) -> Optional[User]:
    """
    Get user by ID
    
    Args:
        db: Database session
        id: User ID
        
    Returns:
        User object or None
    """
    return db.query(User).filter(User.id == id).first()


def get_by_email(db: Session, email: str) -> Optional[User]:
    """
    Get user by email
    
    Args:
        db: Database session
        email: User email
        
    Returns:
        User object or None
    """
    return db.query(User).filter(User.email == email).first()


def get_by_username(db: Session, username: str) -> Optional[User]:
    """
    Get user by username
    
    Args:
        db: Database session
        username: Username
        
    Returns:
        User object or None
    """
    return db.query(User).filter(User.username == username).first()


def create(db: Session, obj_in: UserCreate) -> User:
    """
    Create new user
    
    Args:
        db: Database session
        obj_in: User creation data
        
    Returns:
        Created user object
    """
    db_obj = User(
        email=obj_in.email,
        username=obj_in.username,
        password_hash=get_password_hash(obj_in.password),
        full_name=obj_in.full_name,
        phone=obj_in.phone
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update(db: Session, db_obj: User, obj_in: UserUpdate) -> User:
    """
    Update user
    
    Args:
        db: Database session
        db_obj: User object to update
        obj_in: User update data
        
    Returns:
        Updated user object
    """
    update_data = obj_in.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_obj, field, value)
    
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete(db: Session, id: int) -> Optional[User]:
    """
    Delete user
    
    Args:
        db: Database session
        id: User ID
        
    Returns:
        Deleted user object or None
    """
    obj = db.query(User).filter(User.id == id).first()
    if obj:
        db.delete(obj)
        db.commit()
    return obj


def deactivate(db: Session, id: int) -> Optional[User]:
    """
    Deactivate user (soft delete)
    
    Args:
        db: Database session
        id: User ID
        
    Returns:
        Deactivated user object or None
    """
    obj = db.query(User).filter(User.id == id).first()
    if obj:
        obj.is_active = False
        db.add(obj)
        db.commit()
        db.refresh(obj)
    return obj
