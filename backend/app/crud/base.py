from typing import Any, Dict, Generic, List, Optional, Type, TypeVar
from sqlalchemy import and_
from sqlalchemy.orm import Session

from ..core.database import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """通用 CRUD 基类"""
    
    def __init__(self, model: Type[ModelType]):
        self.model = model
    
    def get(self, db: Session, id: int) -> Optional[ModelType]:
        """根据 ID 获取单个对象"""
        return db.query(self.model).filter(self.model.id == id).first()
    
    def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[ModelType]:
        """获取多个对象（支持分页和过滤）"""
        query = db.query(self.model)
        
        if filters:
            conditions = []
            for key, value in filters.items():
                if value is not None and hasattr(self.model, key):
                    conditions.append(getattr(self.model, key) == value)
            if conditions:
                query = query.filter(and_(*conditions))
        
        return query.offset(skip).limit(limit).all()
    
    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        """创建对象"""
        obj_in_data = obj_in.model_dump() if hasattr(obj_in, 'model_dump') else obj_in.dict()
        obj = self.model(**obj_in_data)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj
    
    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: UpdateSchemaType
    ) -> ModelType:
        """更新对象"""
        obj_data = obj_in.model_dump() if hasattr(obj_in, 'model_dump') else obj_in.dict()
        
        for field, value in obj_data.items():
            if value is not None and hasattr(db_obj, field):
                setattr(db_obj, field, value)
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def remove(self, db: Session, *, id: int) -> ModelType:
        """删除对象"""
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj
