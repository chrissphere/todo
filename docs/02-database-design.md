# 数据库设计

## 一、ER 图概览

```
┌─────────────┐       ┌─────────────┐       ┌─────────────┐
│    User     │       │    List     │       │     Tag     │
├─────────────┤       ├─────────────┤       ├─────────────┤
│ id          │       │ id          │       │ id          │
│ email       │       │ name        │       │ name        │
│ username    │       │ color       │       │ color       │
│ created_at  │       │ icon        │       │ created_at  │
└─────────────┘       │ user_id (FK)│       │ user_id (FK)│
        │             └─────────────┘       └─────────────┘
        │                       │                       │
        │             ┌─────────┴─────────┐             │
        │             │                   │             │
        ▼             ▼                   ▼             ▼
┌─────────────────────────────────────────────────────────────┐
│                          Task                                │
├─────────────────────────────────────────────────────────────┤
│ id                                                          │
│ title                                                       │
│ description                                                 │
│ status (pending/completed/cancelled)                        │
│ priority (high/medium/low/none)                             │
│ due_date                                                    │
│ due_time                                                    │
│ reminder_at                                                 │
│ is_recurring                                                │
│ recurring_rule (JSON)                                       │
│ parent_task_id (FK, self-reference)                         │
│ list_id (FK)                                                │
│ user_id (FK)                                                │
│ created_at                                                  │
│ updated_at                                                  │
│ completed_at                                                │
│ deleted_at (soft delete)                                    │
└─────────────────────────────────────────────────────────────┘
        │
        │
┌───────┴────────┐
│  TaskTag       │ (Many-to-Many junction table)
├────────────────┤
│ task_id (FK)   │
│ tag_id (FK)    │
└────────────────┘
```

## 二、表结构详细设计

### 1. users 表
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) NOT NULL,
    password_hash VARCHAR(255),  -- 如果未来需要登录
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 2. lists 表
```sql
CREATE TABLE lists (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    color VARCHAR(7) DEFAULT '#4A90D9',  -- hex color
    icon VARCHAR(50) DEFAULT 'list',
    sort_order INTEGER DEFAULT 0,
    is_system BOOLEAN DEFAULT FALSE,  -- 系统默认清单不可删除
    user_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP,  -- 软删除
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

### 3. tags 表
```sql
CREATE TABLE tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) NOT NULL,
    color VARCHAR(7) DEFAULT '#4A90D9',
    user_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(name, user_id),  -- 同一用户的标签名唯一
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

### 4. tasks 表
```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(500) NOT NULL,
    description TEXT,
    status VARCHAR(20) DEFAULT 'pending',  -- pending, completed, cancelled
    priority VARCHAR(10) DEFAULT 'none',  -- high, medium, low, none
    due_date DATE,
    due_time TIME,
    reminder_at TIMESTAMP,
    is_recurring BOOLEAN DEFAULT FALSE,
    recurring_rule JSON,  -- {"type": "daily", "interval": 1, "end_date": null}
    parent_task_id INTEGER,  -- 子任务关联
    list_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    sort_order INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    deleted_at TIMESTAMP,  -- 软删除
    FOREIGN KEY (parent_task_id) REFERENCES tasks(id) ON DELETE SET NULL,
    FOREIGN KEY (list_id) REFERENCES lists(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 索引优化
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_list_id ON tasks(list_id);
CREATE INDEX idx_tasks_parent_task_id ON tasks(parent_task_id);
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_priority ON tasks(priority);
CREATE INDEX idx_tasks_due_date ON tasks(due_date);
CREATE INDEX idx_tasks_deleted_at ON tasks(deleted_at);
CREATE INDEX idx_tasks_user_status ON tasks(user_id, status);
```

### 5. task_tags 表（多对多关联）
```sql
CREATE TABLE task_tags (
    task_id INTEGER NOT NULL,
    tag_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (task_id, tag_id),
    FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
);

CREATE INDEX idx_task_tags_task_id ON task_tags(task_id);
CREATE INDEX idx_task_tags_tag_id ON task_tags(tag_id);
```

## 三、recurring_rule JSON 结构示例

```json
// 每天重复
{
  "type": "daily",
  "interval": 1,
  "end_date": null
}

// 每 2 周重复
{
  "type": "weekly",
  "interval": 2,
  "days_of_week": [1, 3, 5],  // 周一、三、五
  "end_date": "2026-12-31"
}

// 每月重复（每月 15 号）
{
  "type": "monthly",
  "interval": 1,
  "day_of_month": 15,
  "end_date": null
}

// 每年重复
{
  "type": "yearly",
  "interval": 1,
  "month": 6,
  "day": 15,
  "end_date": null
}
```

## 四、系统默认清单

初始化时为每个用户创建以下系统清单：

1. **收件箱 (Inbox)** - icon: inbox, color: #4A90D9
2. **今天 (Today)** - icon: calendar-today, color: #FF6B6B (虚拟清单，动态筛选)
3. **下一步 (Next 7 Days)** - icon: calendar-week, color: #FFA500 (虚拟清单)
4. **日程表 (Schedule)** - icon: calendar, color: #9370DB (显示所有有日期的任务)

注意：Today 和 Next 7 Days 是虚拟清单，通过查询条件实现，不实际存储。

## 五、数据迁移策略

使用 Alembic 进行数据库迁移管理：

```bash
# 初始化 Alembic
alembic init alembic

# 创建迁移
alembic revision --autogenerate -m "Initial schema"

# 应用迁移
alembic upgrade head
```
