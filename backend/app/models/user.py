from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text, Date, Time, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from ..core.database import Base


class User(Base):
    """用户模型"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=True)  # 可选，用于未来登录
    username = Column(String(100), nullable=False, default="default_user")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 关系
    lists = relationship("List", back_populates="user", cascade="all, delete-orphan")
    tags = relationship("Tag", back_populates="user", cascade="all, delete-orphan")
    tasks = relationship("Task", back_populates="user", cascade="all, delete-orphan")
