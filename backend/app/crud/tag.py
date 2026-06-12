from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime

from ..models.tag import Tag
from ..schemas.tag import TagCreate, TagUpdate


class CRUDTag:
    """标签 CRUD 操作"""
    
    def get(self, db: Session, id: int) -> Optional[Tag]:
        """根据 ID 获取标签"""
        return db.query(Tag).filter(Tag.id == id).first()
    
    def get_multi(self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100) -> List[Tag]:
        """获取标签列表"""
        return db.query(Tag).filter(
            Tag.user_id == user_id
        ).order_by(Tag.created_at).offset(skip).limit(limit).all()
    
    def create(self, db: Session, *, obj_in: TagCreate, user_id: int) -> Tag:
        """创建标签"""
        data = obj_in.model_dump()
        data['user_id'] = user_id
        
        obj = Tag(**data)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj
    
    def update(self, db: Session, *, db_obj: Tag, obj_in: TagUpdate) -> Tag:
        """更新标签"""
        data = obj_in.model_dump(exclude_unset=True)
        
        for field, value in data.items():
            setattr(db_obj, field, value)
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def remove(self, db: Session, *, id: int) -> Tag:
        """删除标签"""
        obj = self.get(db, id=id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj
    
    def get_by_user(self, db: Session, user_id: int) -> List[Tag]:
        """获取用户的所有标签"""
        return db.query(Tag).filter(Tag.user_id == user_id).all()
