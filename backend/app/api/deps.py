"""
API dependencies
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.security import decode_token, verify_token_type
from app.crud import user as crud_user
from app.models.user import User


# HTTP Bearer token security
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Get current authenticated user
    
    Args:
        credentials: HTTP Bearer token credentials
        db: Database session
        
    Returns:
        Current user
        
    Raises:
        HTTPException: If token is invalid or user not found
    """
    token = credentials.credentials
    
    # Decode token
    payload = decode_token(token)
    
    # Verify token type
    if not verify_token_type(payload, "access"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type"
        )
    
    # Get user ID from token
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
    
    # Get user from database
    user = crud_user.get(db, id=int(user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    
    return user


async def get_current_admin_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Get current authenticated admin user
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        Current admin user
        
    Raises:
        HTTPException: If user is not an admin
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return current_user
