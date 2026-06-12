# Todo App - 滴答清单风格的待办事项系统

一个现代化的待办事项管理系统，支持任务管理、清单分类、日期提醒、优先级、标签、子任务和重复任务等功能。

## 🚀 快速开始

### 后端启动

```bash
cd backend

# 创建虚拟环境
python -m venv .venv
source .venv/bin/activate  # Linux/macOS

# 安装依赖
pip install -r requirements.txt

# 初始化数据库
python init_db.py

# 启动服务器
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

访问 API 文档：http://localhost:8000/api/v1/docs

### 前端启动（开发中）

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

## 📋 核心功能

### ✅ 任务管理
- 创建、编辑、删除任务
- 标记任务完成/未完成
- 任务详情查看
- 任务排序

### 📝 清单管理
- 多个清单分类
- 系统默认清单（收件箱、今天、下一步、日程表）
- 自定义清单颜色和图标

### 📅 时间管理
- 截止日期设置
- 具体时间设置
- 提醒功能
- 重复任务（每天、每周、每月）

### 🎯 优先级系统
- 四级优先级：高、中、低、无
- 颜色标识
- 优先级筛选

### 🏷️ 标签系统
- 创建和管理标签
- 标签颜色自定义
- 跨清单分类

### 📊 子任务
- 任务分解
- 进度追踪
- 独立属性

### 🔍 搜索和过滤
- 全文搜索
- 高级筛选
- 智能视图（今天、过期）

## 🛠️ 技术栈

### 后端
- **FastAPI** - 现代高性能 Web 框架
- **SQLAlchemy** - ORM 框架
- **SQLite** - 数据库（支持切换到 PostgreSQL/MySQL）
- **Alembic** - 数据库迁移
- **Pydantic** - 数据验证

### 前端（开发中）
- **Vue 3** - 渐进式 JavaScript 框架
- **Element Plus** - Vue 3 组件库
- **Pinia** - 状态管理
- **Vue Router** - 路由管理
- **Axios** - HTTP 客户端

### 部署
- **Docker** - 容器化部署
- **Docker Compose** - 多容器编排

## 📁 项目结构

```
todo-app/
├── backend/                 # 后端 API
│   ├── app/
│   │   ├── api/            # API 路由
│   │   ├── core/           # 核心配置
│   │   ├── crud/           # CRUD 操作
│   │   ├── models/         # 数据模型
│   │   ├── schemas/        # Pydantic Schemas
│   │   └── main.py         # FastAPI 入口
│   ├── alembic/            # 数据库迁移
│   ├── requirements.txt    # Python 依赖
│   └── init_db.py          # 初始化脚本
├── frontend/               # 前端应用（开发中）
│   └── src/
├── docker/                 # Docker 配置（开发中）
│   └── nginx/
└── docs/                   # 项目文档
    ├── 01-requirements-analysis.md
    ├── 02-database-design.md
    └── 03-development-tasks.md
```

## 📖 API 文档

启动后端后访问：
- Swagger UI: http://localhost:8000/api/v1/docs
- ReDoc: http://localhost:8000/api/v1/redoc
- OpenAPI JSON: http://localhost:8000/api/v1/openapi.json

### 主要 API 端点

#### Tasks（任务）
```
GET    /api/v1/tasks              # 获取任务列表
POST   /api/v1/tasks              # 创建任务
GET    /api/v1/tasks/{id}         # 获取任务详情
PUT    /api/v1/tasks/{id}         # 更新任务
PATCH  /api/v1/tasks/{id}/complete # 完成任务
DELETE /api/v1/tasks/{id}         # 删除任务
GET    /api/v1/tasks/today        # 今天的任务
GET    /api/v1/tasks/overdue      # 过期的任务
GET    /api/v1/tasks/search?q=    # 搜索任务
```

#### Lists（清单）
```
GET    /api/v1/lists              # 获取所有清单
POST   /api/v1/lists              # 创建清单
GET    /api/v1/lists/{id}         # 获取清单详情
PUT    /api/v1/lists/{id}         # 更新清单
DELETE /api/v1/lists/{id}         # 删除清单
```

#### Tags（标签）
```
GET    /api/v1/tags               # 获取所有标签
POST   /api/v1/tags               # 创建标签
PUT    /api/v1/tags/{id}          # 更新标签
DELETE /api/v1/tags/{id}          # 删除标签
```

## 🔧 开发指南

### 数据库迁移

```bash
cd backend

# 创建新迁移
alembic revision --autogenerate -m "描述"

# 应用迁移
alembic upgrade head

# 回滚迁移
alembic downgrade -1
```

### 运行测试

```bash
cd backend
pytest tests/
```

## 📝 开发进度

- [x] 需求分析和功能模块拆解
- [x] 数据库设计
- [x] 后端基础架构
- [x] 后端 API（核心 CRUD）
- [ ] 后端 API（高级功能）
- [ ] 前端项目初始化
- [ ] 前端页面和组件
- [ ] Docker 配置
- [ ] 测试和文档

## 🚧 待实现功能

### P1 - 核心体验
- [ ] 子任务功能完善
- [ ] 任务标签关联 API
- [ ] 重复任务逻辑实现
- [ ] 前端界面开发

### P2 - 增强功能
- [ ] 复杂重复规则
- [ ] 多个提醒
- [ ] 任务评论
- [ ] 任务附件
- [ ] 用户认证系统
- [ ] 协作功能

## 📄 许可证

MIT License

## 👥 贡献

欢迎提交 Issue 和 Pull Request！
