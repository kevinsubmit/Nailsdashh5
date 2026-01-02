"""
Verification Code database model for phone verification
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, func
from app.db.session import Base


class VerificationCode(Base):
    """Verification code model for phone verification"""
    __tablename__ = "verification_codes"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    phone = Column(String(20), nullable=False, index=True)  # 手机号
    code = Column(String(6), nullable=False)  # 验证码（6位数字）
    purpose = Column(String(50), nullable=False)  # 用途：register, login, reset_password
    is_used = Column(Boolean, default=False, nullable=False)  # 是否已使用
    expires_at = Column(DateTime(timezone=True), nullable=False)  # 过期时间
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<VerificationCode(phone={self.phone}, purpose={self.purpose}, is_used={self.is_used})>"
