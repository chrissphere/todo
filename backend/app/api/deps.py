from typing import Optional
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..core.database import get_db


def get_current_user(db: Session = Depends(get_db)) -> dict:
    """
    获取当前用户（临时实现）
    
    TODO: 实现真实的用户认证系统
    目前返回一个 mock 用户用于开发测试
    """
    # 临时返回一个默认用户
    return {"id": 1, "username": "test_user"}
