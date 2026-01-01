"""
User Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=100)
    full_name: Optional[str] = Field(None, max_length=200)
    phone: Optional[str] = Field(None, max_length=20)


class UserCreate(UserBase):
    """Schema for user registration"""
    password: str = Field(..., min_length=8, max_length=100)


class UserUpdate(BaseModel):
    """Schema for user update"""
    full_name: Optional[str] = Field(None, max_length=200)
    phone: Optional[str] = Field(None, max_length=20)
    avatar_url: Optional[str] = Field(None, max_length=500)


class UserInDB(UserBase):
    """Schema for user in database"""
    id: int
    avatar_url: Optional[str] = None
    is_active: bool
    is_admin: bool
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class UserResponse(UserInDB):
    """Schema for user response (excludes sensitive data)"""
    pass


class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr
    password: str


class Token(BaseModel):
    """Schema for JWT token response"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema for token payload data"""
    user_id: Optional[int] = None
    email: Optional[str] = None
