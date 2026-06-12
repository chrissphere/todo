from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text, Date, Time, JSON, Index
from sqlalchemy.orm import relationship
from datetime import datetime
from ..core.database import Base


class Task(Base):
    """任务模型"""
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(20), default="pending")  # pending, completed, cancelled
    priority = Column(String(10), default="none")  # high, medium, low, none
    due_date = Column(Date, nullable=True)
    due_time = Column(Time, nullable=True)
    reminder_at = Column(DateTime, nullable=True)
    is_recurring = Column(Boolean, default=False)
    recurring_rule = Column(JSON, nullable=True)  # {"type": "daily", "interval": 1, ...}
    parent_task_id = Column(Integer, ForeignKey("tasks.id", ondelete="SET NULL"), nullable=True)
    list_id = Column(Integer, ForeignKey("lists.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    sort_order = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    deleted_at = Column(DateTime, nullable=True)  # 软删除
    
    # 关系
    user = relationship("User", back_populates="tasks")
    list = relationship("List", back_populates="tasks")
    parent = relationship("Task", remote_side=[id], backref="children", foreign_keys=[parent_task_id])
    tags = relationship("Tag", secondary="task_tags", back_populates="tasks")
    
    # 索引
    __table_args__ = (
        Index('idx_tasks_user_id', 'user_id'),
        Index('idx_tasks_list_id', 'list_id'),
        Index('idx_tasks_parent_task_id', 'parent_task_id'),
        Index('idx_tasks_status', 'status'),
        Index('idx_tasks_priority', 'priority'),
        Index('idx_tasks_due_date', 'due_date'),
        Index('idx_tasks_deleted_at', 'deleted_at'),
        Index('idx_tasks_user_status', 'user_id', 'status'),
    )
