from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..api.deps import get_current_user
from ..crud.task import crud_task
from ..schemas.task import TaskCreate, TaskUpdate, TaskResponse

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("", response_model=List[TaskResponse])
def get_tasks(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    list_id: Optional[int] = Query(None, description="清单 ID"),
    status: Optional[str] = Query(None, description="任务状态"),
    priority: Optional[str] = Query(None, description="优先级"),
    tag_id: Optional[int] = Query(None, description="标签 ID"),
    skip: int = Query(0, ge=0, description="跳过数量"),
    limit: int = Query(100, ge=1, le=1000, description="返回数量上限")
):
    """获取任务列表"""
    tasks = crud_task.get_multi(
        db,
        user_id=current_user["id"],
        skip=skip,
        limit=limit,
        list_id=list_id,
        status=status,
        priority=priority,
        tag_id=tag_id
    )
    return tasks


@router.get("/today", response_model=List[TaskResponse])
def get_today_tasks(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """获取今天的任务"""
    tasks = crud_task.get_today_tasks(db, user_id=current_user["id"])
    return tasks


@router.get("/overdue", response_model=List[TaskResponse])
def get_overdue_tasks(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """获取过期的任务"""
    tasks = crud_task.get_overdue_tasks(db, user_id=current_user["id"])
    return tasks


@router.get("/search", response_model=List[TaskResponse])
def search_tasks(
    q: str = Query(..., min_length=1, description="搜索关键词"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """搜索任务"""
    tasks = crud_task.search(db, user_id=current_user["id"], query=q)
    return tasks


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """获取单个任务详情"""
    task = crud_task.get(db, id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    if task.user_id != current_user["id"]:
        raise HTTPException(status_code=403, detail="无权访问此任务")
    return task


@router.post("", response_model=TaskResponse)
def create_task(
    task_in: TaskCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """创建新任务"""
    task = crud_task.create(db, obj_in=task_in, user_id=current_user["id"])
    return task


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_in: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """更新任务"""
    task = crud_task.get(db, id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    if task.user_id != current_user["id"]:
        raise HTTPException(status_code=403, detail="无权访问此任务")
    
    task = crud_task.update(db, db_obj=task, obj_in=task_in)
    return task


@router.patch("/{task_id}/complete", response_model=TaskResponse)
def complete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """完成任务"""
    task = crud_task.get(db, id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    if task.user_id != current_user["id"]:
        raise HTTPException(status_code=403, detail="无权访问此任务")
    
    task = crud_task.complete(db, db_obj=task)
    return task


@router.delete("/{task_id}", response_model=TaskResponse)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """删除任务（软删除）"""
    task = crud_task.get(db, id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    if task.user_id != current_user["id"]:
        raise HTTPException(status_code=403, detail="无权访问此任务")
    
    task = crud_task.remove(db, id=task_id)
    return task


@router.get("/lists/{list_id}", response_model=List[TaskResponse])
def get_tasks_by_list(
    list_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """获取清单下的所有任务"""
    tasks = crud_task.get_by_list(db, list_id=list_id, user_id=current_user["id"])
    return tasks
