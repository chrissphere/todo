from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, and_
from datetime import datetime, date

from ..models.task import Task
from ..schemas.task import TaskCreate, TaskUpdate


class CRUDTask:
    """任务 CRUD 操作"""
    
    def get(self, db: Session, id: int) -> Optional[Task]:
        """根据 ID 获取任务"""
        return db.query(Task).filter(Task.id == id, Task.deleted_at.is_(None)).first()
    
    def get_multi(
        self,
        db: Session,
        *,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        list_id: Optional[int] = None,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        tag_id: Optional[int] = None
    ) -> List[Task]:
        """获取任务列表（支持过滤）"""
        query = db.query(Task).filter(
            Task.user_id == user_id,
            Task.deleted_at.is_(None)
        )
        
        if list_id is not None:
            query = query.filter(Task.list_id == list_id)
        
        if status is not None:
            query = query.filter(Task.status == status)
        
        if priority is not None:
            query = query.filter(Task.priority == priority)
        
        if tag_id is not None:
            query = query.join(Task.tags).filter(Task.tags.any(id=tag_id))
        
        return query.order_by(Task.sort_order, Task.created_at).offset(skip).limit(limit).all()
    
    def get_today_tasks(self, db: Session, user_id: int) -> List[Task]:
        """获取今天的任务"""
        today = date.today()
        return db.query(Task).filter(
            Task.user_id == user_id,
            Task.due_date == today,
            Task.deleted_at.is_(None),
            Task.status == "pending"
        ).all()
    
    def get_overdue_tasks(self, db: Session, user_id: int) -> List[Task]:
        """获取过期的任务"""
        today = date.today()
        return db.query(Task).filter(
            Task.user_id == user_id,
            Task.due_date < today,
            Task.deleted_at.is_(None),
            Task.status == "pending"
        ).all()
    
    def search(self, db: Session, user_id: int, query: str) -> List[Task]:
        """搜索任务"""
        search_pattern = f"%{query}%"
        return db.query(Task).filter(
            Task.user_id == user_id,
            Task.deleted_at.is_(None),
            or_(
                Task.title.ilike(search_pattern),
                Task.description.ilike(search_pattern)
            )
        ).all()
    
    def create(self, db: Session, *, obj_in: TaskCreate, user_id: int) -> Task:
        """创建任务"""
        data = obj_in.model_dump(exclude={'tag_ids'})
        data['user_id'] = user_id
        
        obj = Task(**data)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        
        # 处理标签关联
        if obj_in.tag_ids:
            from ..models.task_tag import TaskTag
            for tag_id in obj_in.tag_ids:
                task_tag = TaskTag(task_id=obj.id, tag_id=tag_id)
                db.add(task_tag)
            db.commit()
            db.refresh(obj)
        
        return obj
    
    def update(self, db: Session, *, db_obj: Task, obj_in: TaskUpdate) -> Task:
        """更新任务"""
        data = obj_in.model_dump(exclude_unset=True, exclude={'tag_ids'})
        
        for field, value in data.items():
            setattr(db_obj, field, value)
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        
        # 处理标签关联
        if obj_in.tag_ids is not None:
            from ..models.task_tag import TaskTag
            # 删除旧标签
            db.query(TaskTag).filter(TaskTag.task_id == db_obj.id).delete()
            # 添加新标签
            for tag_id in obj_in.tag_ids:
                task_tag = TaskTag(task_id=db_obj.id, tag_id=tag_id)
                db.add(task_tag)
            db.commit()
            db.refresh(db_obj)
        
        return db_obj
    
    def complete(self, db: Session, *, db_obj: Task) -> Task:
        """完成任务"""
        db_obj.status = "completed"
        db_obj.completed_at = datetime.utcnow()
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def remove(self, db: Session, *, id: int) -> Task:
        """软删除任务"""
        obj = self.get(db, id=id)
        if obj:
            obj.deleted_at = datetime.utcnow()
            db.add(obj)
            db.commit()
            db.refresh(obj)
        return obj
    
    def get_by_list(self, db: Session, list_id: int, user_id: int) -> List[Task]:
        """获取清单下的所有任务"""
        return db.query(Task).filter(
            Task.list_id == list_id,
            Task.user_id == user_id,
            Task.deleted_at.is_(None)
        ).order_by(Task.sort_order, Task.created_at).all()
