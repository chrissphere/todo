from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from ..core.database import Base


class Tag(Base):
    """标签模型"""
    __tablename__ = "tags"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    color = Column(String(7), default="#4A90D9")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 唯一约束：同一用户的标签名唯一
    __table_args__ = (
        UniqueConstraint('name', 'user_id', name='uq_tag_name_user_id'),
    )
    
    # 关系
    user = relationship("User", back_populates="tags")
    tasks = relationship("Task", secondary="task_tags", back_populates="tags")
