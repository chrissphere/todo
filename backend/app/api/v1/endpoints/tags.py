from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..api.deps import get_current_user
from ..crud.tag import crud_tag
from ..schemas.tag import TagCreate, TagUpdate, TagResponse

router = APIRouter(prefix="/tags", tags=["tags"])


@router.get("", response_model=List[TagResponse])
def get_tags(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """获取所有标签"""
    tags = crud_tag.get_multi(db, user_id=current_user["id"])
    return tags


@router.get("/{tag_id}", response_model=TagResponse)
def get_tag(
    tag_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """获取单个标签"""
    tag = crud_tag.get(db, id=tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="标签不存在")
    return tag


@router.post("", response_model=TagResponse)
def create_tag(
    tag_in: TagCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """创建新标签"""
    tag = crud_tag.create(db, obj_in=tag_in, user_id=current_user["id"])
    return tag


@router.put("/{tag_id}", response_model=TagResponse)
def update_tag(
    tag_id: int,
    tag_in: TagUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """更新标签"""
    tag = crud_tag.get(db, id=tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="标签不存在")
    
    tag = crud_tag.update(db, db_obj=tag, obj_in=tag_in)
    return tag


@router.delete("/{tag_id}", response_model=TagResponse)
def delete_tag(
    tag_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """删除标签"""
    tag = crud_tag.get(db, id=tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="标签不存在")
    
    tag = crud_tag.remove(db, id=tag_id)
    return tag
