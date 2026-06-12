from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from ..core.database import Base


class List(Base):
    """清单模型"""
    __tablename__ = "lists"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    color = Column(String(7), default="#4A90D9")  # hex color
    icon = Column(String(50), default="list")
    sort_order = Column(Integer, default=0)
    is_system = Column(Boolean, default=False)  # 系统默认清单不可删除
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)  # 软删除
    
    # 关系
    user = relationship("User", back_populates="lists")
    tasks = relationship("Task", back_populates="list", cascade="all, delete-orphan")
