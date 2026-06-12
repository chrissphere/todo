from fastapi import APIRouter

from .endpoints import tasks, lists, tags

# API v1 路由器
api_router = APIRouter()

# 注册路由
api_router.include_router(tasks.router)
api_router.include_router(lists.router)
api_router.include_router(tags.router)
