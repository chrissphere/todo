from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..api.deps import get_current_user
from ..crud.list import crud_list
from ..schemas.list import ListCreate, ListUpdate, ListResponse

router = APIRouter(prefix="/lists", tags=["lists"])


@router.get("", response_model=List[ListResponse])
def get_lists(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """获取所有清单"""
    lists = crud_list.get_multi(db, user_id=current_user["id"])
    return lists


@router.get("/{list_id}", response_model=ListResponse)
def get_list(
    list_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """获取单个清单"""
    list_obj = crud_list.get(db, id=list_id)
    if not list_obj:
        raise HTTPException(status_code=404, detail="清单不存在")
    if list_obj.user_id != current_user["id"]:
        raise HTTPException(status_code=403, detail="无权访问此清单")
    return list_obj


@router.post("", response_model=ListResponse)
def create_list(
    list_in: ListCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """创建新清单"""
    list_obj = crud_list.create(db, obj_in=list_in, user_id=current_user["id"])
    return list_obj


@router.put("/{list_id}", response_model=ListResponse)
def update_list(
    list_id: int,
    list_in: ListUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """更新清单"""
    list_obj = crud_list.get(db, id=list_id)
    if not list_obj:
        raise HTTPException(status_code=404, detail="清单不存在")
    if list_obj.user_id != current_user["id"]:
        raise HTTPException(status_code=403, detail="无权访问此清单")
    
    list_obj = crud_list.update(db, db_obj=list_obj, obj_in=list_in)
    return list_obj


@router.delete("/{list_id}", response_model=ListResponse)
def delete_list(
    list_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """删除清单"""
    list_obj = crud_list.get(db, id=list_id)
    if not list_obj:
        raise HTTPException(status_code=404, detail="清单不存在")
    if list_obj.user_id != current_user["id"]:
        raise HTTPException(status_code=403, detail="无权访问此清单")
    if list_obj.is_system:
        raise HTTPException(status_code=400, detail="系统清单不可删除")
    
    list_obj = crud_list.remove(db, id=list_id)
    return list_obj
