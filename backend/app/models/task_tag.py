from sqlalchemy import Column, Integer, ForeignKey, DateTime
from datetime import datetime
from ..core.database import Base


class TaskTag(Base):
    """任务 - 标签多对多关联表"""
    __tablename__ = "task_tags"
    
    task_id = Column(Integer, ForeignKey("tasks.id", ondelete="CASCADE"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
