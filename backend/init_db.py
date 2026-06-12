#!/usr/bin/env python3
"""
初始化数据库脚本
创建默认用户和系统清单
"""

import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from sqlalchemy.orm import Session
from app.core.database import engine, Base, SessionLocal
from app.models import User, List

def init_db():
    """初始化数据库"""
    print("创建数据库表...")
    Base.metadata.create_all(bind=engine)
    
    print("创建默认用户和系统清单...")
    db = SessionLocal()
    
    try:
        # 创建默认用户
        user = db.query(User).filter(User.username == "default_user").first()
        if not user:
            user = User(username="default_user", email=None)
            db.add(user)
            db.commit()
            db.refresh(user)
            print(f"✓ 创建默认用户：ID={user.id}, username={user.username}")
        else:
            print(f"✓ 默认用户已存在：ID={user.id}")
        
        # 创建系统清单
        system_lists = [
            {"name": "收件箱", "icon": "inbox", "color": "#4A90D9"},
            {"name": "今天", "icon": "calendar-today", "color": "#FF6B6B"},
            {"name": "下一步", "icon": "calendar-week", "color": "#FFA500"},
            {"name": "日程表", "icon": "calendar", "color": "#9370DB"},
        ]
        
        for list_data in system_lists:
            existing = db.query(List).filter(
                List.user_id == user.id,
                List.name == list_data["name"]
            ).first()
            
            if not existing:
                system_list = List(
                    name=list_data["name"],
                    icon=list_data["icon"],
                    color=list_data["color"],
                    user_id=user.id,
                    is_system=True
                )
                db.add(system_list)
                print(f"  ✓ 创建系统清单：{list_data['name']}")
            else:
                print(f"  ✓ 系统清单已存在：{list_data['name']}")
        
        db.commit()
        print("\n✓ 数据库初始化完成！")
        
    except Exception as e:
        db.rollback()
        print(f"\n✗ 初始化失败：{e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
