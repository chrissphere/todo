"""CRUD 操作导出"""
from .task import CRUDTask
from .list import CRUDList
from .tag import CRUDTag

crud_task = CRUDTask()
crud_list = CRUDList()
crud_tag = CRUDTag()

__all__ = ["crud_task", "crud_list", "crud_tag", "CRUDTask", "CRUDList", "CRUDTag"]
