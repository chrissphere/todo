# Todo App Backend

基于 FastAPI + SQLAlchemy 的待办事项系统后端 API。

## 技术栈

- **FastAPI** - 现代高性能 Web 框架
- **SQLAlchemy** - ORM 框架
- **SQLite** - 数据库（可轻松切换到 PostgreSQL/MySQL）
- **Alembic** - 数据库迁移工具
- **Pydantic** - 数据验证

## 快速开始

### 1. 创建虚拟环境

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# 或
.venv\Scripts\activate  # Windows
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件配置数据库等参数
```

### 4. 初始化数据库

```bash
# 运行迁移
alembic upgrade head
```

### 5. 启动服务器

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

访问 http://localhost:8000/api/v1/docs 查看 API 文档。

## API 端点

### Tasks（任务）

- `GET /api/v1/tasks` - 获取任务列表
- `GET /api/v1/tasks/{task_id}` - 获取单个任务
- `POST /api/v1/tasks` - 创建任务
- `PUT /api/v1/tasks/{task_id}` - 更新任务
- `PATCH /api/v1/tasks/{task_id}/complete` - 完成任务
- `DELETE /api/v1/tasks/{task_id}` - 删除任务
- `GET /api/v1/tasks/today` - 获取今天的任务
- `GET /api/v1/tasks/overdue` - 获取过期的任务
- `GET /api/v1/tasks/search?q=xxx` - 搜索任务

### Lists（清单）

- `GET /api/v1/lists` - 获取所有清单
- `GET /api/v1/lists/{list_id}` - 获取单个清单
- `POST /api/v1/lists` - 创建清单
- `PUT /api/v1/lists/{list_id}` - 更新清单
- `DELETE /api/v1/lists/{list_id}` - 删除清单

### Tags（标签）

- `GET /api/v1/tags` - 获取所有标签
- `GET /api/v1/tags/{tag_id}` - 获取单个标签
- `POST /api/v1/tags` - 创建标签
- `PUT /api/v1/tags/{tag_id}` - 更新标签
- `DELETE /api/v1/tags/{tag_id}` - 删除标签

## 数据库迁移

```bash
# 创建新迁移
alembic revision --autogenerate -m "描述"

# 应用迁移
alembic upgrade head

# 回滚迁移
alembic downgrade -1

# 查看迁移历史
alembic history
```

## 项目结构

```
backend/
├── app/
│   ├── api/              # API 路由
│   │   └── v1/
│   │       └── endpoints/
│   ├── core/             # 核心配置
│   ├── crud/             # CRUD 操作
│   ├── models/           # SQLAlchemy 模型
│   ├── schemas/          # Pydantic Schemas
│   └── main.py           # FastAPI 入口
├── alembic/              # 数据库迁移
├── requirements.txt      # Python 依赖
└── .env.example          # 环境变量示例
```

## 开发注意事项

1. **LSP 警告**: SQLAlchemy 和 Alembic 的导入警告是因为虚拟环境未激活，实际运行时正常
2. **用户认证**: 当前使用 mock 用户，生产环境需实现真实认证
3. **数据库**: 默认 SQLite，可通过修改 `DATABASE_URL` 切换到其他数据库

## TODO

- [ ] 实现用户认证系统（JWT）
- [ ] 添加任务评论功能
- [ ] 添加任务附件功能
- [ ] 实现协作功能（共享清单）
- [ ] 添加数据导出/导入功能
- [ ] 实现 WebSocket 实时通知
