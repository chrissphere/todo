from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date, time
from enum import Enum


class TaskStatus(str, Enum):
    """任务状态枚举"""
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Priority(str, Enum):
    """优先级枚举"""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    NONE = "none"


class TaskBase(BaseModel):
    """任务基础 Schema"""
    title: str = Field(..., min_length=1, max_length=500, description="任务标题")
    description: Optional[str] = Field(None, description="任务描述")
    priority: Priority = Field(Priority.NONE, description="优先级")
    status: TaskStatus = Field(TaskStatus.PENDING, description="状态")
    due_date: Optional[date] = Field(None, description="截止日期")
    due_time: Optional[time] = Field(None, description="截止时间")
    reminder_at: Optional[datetime] = Field(None, description="提醒时间")
    is_recurring: bool = Field(False, description="是否重复任务")
    recurring_rule: Optional[dict] = Field(None, description="重复规则")
    list_id: int = Field(..., description="所属清单 ID")
    parent_task_id: Optional[int] = Field(None, description="父任务 ID")
    tag_ids: Optional[List[int]] = Field(None, description="标签 ID 列表")


class TaskCreate(TaskBase):
    """创建任务 Schema"""
    pass


class TaskUpdate(BaseModel):
    """更新任务 Schema（所有字段可选）"""
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    description: Optional[str] = None
    priority: Optional[Priority] = None
    status: Optional[TaskStatus] = None
    due_date: Optional[date] = None
    due_time: Optional[time] = None
    reminder_at: Optional[datetime] = None
    is_recurring: Optional[bool] = None
    recurring_rule: Optional[dict] = None
    list_id: Optional[int] = None
    parent_task_id: Optional[int] = None
    tag_ids: Optional[List[int]] = None
    sort_order: Optional[int] = None


class TaskInDB(TaskBase):
    """数据库中的任务 Schema"""
    id: int
    user_id: int
    sort_order: int
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class TaskResponse(TaskInDB):
    """API 响应任务 Schema"""
    children: Optional[List["TaskResponse"]] = None
    tags: Optional[List["TagResponse"]] = None


class TagBase(BaseModel):
    """标签基础 Schema"""
    name: str = Field(..., min_length=1, max_length=50, description="标签名称")
    color: str = Field("#4A90D9", min_length=4, max_length=7, description="标签颜色")


class TagCreate(TagBase):
    """创建标签 Schema"""
    pass


class TagUpdate(BaseModel):
    """更新标签 Schema"""
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    color: Optional[str] = Field(None, min_length=4, max_length=7)


class TagResponse(TagBase):
    """标签响应 Schema"""
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class ListBase(BaseModel):
    """清单基础 Schema"""
    name: str = Field(..., min_length=1, max_length=100, description="清单名称")
    color: str = Field("#4A90D9", min_length=4, max_length=7, description="清单颜色")
    icon: str = Field("list", description="清单图标")
    sort_order: int = Field(0, description="排序顺序")


class ListCreate(ListBase):
    """创建清单 Schema"""
    pass


class ListUpdate(BaseModel):
    """更新清单 Schema"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    color: Optional[str] = Field(None, min_length=4, max_length=7)
    icon: Optional[str] = Field(None)
    sort_order: Optional[int] = None


class ListResponse(ListBase):
    """清单响应 Schema"""
    id: int
    user_id: int
    is_system: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ListWithTasks(ListResponse):
    """包含任务的清单 Schema"""
    tasks: Optional[List[TaskResponse]] = None


# 更新 TaskResponse 以支持前向引用
TaskResponse.model_rebuild()
