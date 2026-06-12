from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime

from ..models.list import List
from ..schemas.list import ListCreate, ListUpdate


class CRUDList:
    """清单 CRUD 操作"""
    
    def get(self, db: Session, id: int) -> Optional[List]:
        """根据 ID 获取清单"""
        return db.query(List).filter(
            List.id == id,
            List.deleted_at.is_(None)
        ).first()
    
    def get_multi(self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100) -> List[List]:
        """获取清单列表"""
        return db.query(List).filter(
            List.user_id == user_id,
            List.deleted_at.is_(None)
        ).order_by(List.sort_order, List.created_at).offset(skip).limit(limit).all()
    
    def create(self, db: Session, *, obj_in: ListCreate, user_id: int) -> List:
        """创建清单"""
        data = obj_in.model_dump()
        data['user_id'] = user_id
        
        obj = List(**data)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj
    
    def update(self, db: Session, *, db_obj: List, obj_in: ListUpdate) -> List:
        """更新清单"""
        data = obj_in.model_dump(exclude_unset=True)
        
        for field, value in data.items():
            setattr(db_obj, field, value)
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def remove(self, db: Session, *, id: int) -> List:
        """软删除清单"""
        obj = self.get(db, id=id)
        if obj and not obj.is_system:
            obj.deleted_at = datetime.utcnow()
            db.add(obj)
            db.commit()
            db.refresh(obj)
        return obj
    
    def get_by_user(self, db: Session, user_id: int) -> List[List]:
        """获取用户的所有清单"""
        return db.query(List).filter(
            List.user_id == user_id,
            List.deleted_at.is_(None)
        ).order_by(List.sort_order).all()
