# 待办事项系统 (Todo App)

类似滴答清单的任务管理系统 - 支持任务管理、清单分类、优先级、提醒、重复任务等功能。

![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/chrissphere/todo/ci.yml?branch=main)
![Docker Pulls](https://img.shields.io/docker/pulls/chrissphere/todo-backend)
![License](https://img.shields.io/github/license/chrissphere/todo)

## ✨ 功能特性

### 任务管理
- ✅ 创建、编辑、删除任务
- ✅ 任务完成状态切换
- ✅ 优先级设置（高/中/低）
- ✅ 截止日期和提醒时间
- ✅ 子任务支持
- ✅ 任务排序和拖拽

### 清单管理
- 📁 多个清单分类
- 🎨 自定义颜色和图标
- 📊 按清单过滤任务

### 标签系统
- 🏷️ 多标签分类
- 🔍 按标签搜索

### 高级功能
- 🔄 重复任务（每天/每周/每月）
- 🔔 桌面通知
- 🌙 深色模式
- 📱 响应式设计

## 🛠️ 技术栈

### 后端
- **框架**: FastAPI
- **数据库**: SQLite (可切换 PostgreSQL)
- **ORM**: SQLAlchemy 2.0
- **迁移**: Alembic
- **验证**: Pydantic

### 前端
- **框架**: Vue 3 + TypeScript
- **构建**: Vite
- **UI**: Element Plus
- **状态**: Pinia
- **路由**: Vue Router

### 部署
- **容器**: Docker + Docker Compose
- **CI/CD**: GitHub Actions
- **镜像**: Docker Hub

## 🚀 快速开始

### 使用 Docker Compose（推荐）

```bash
# 克隆仓库
git clone https://github.com/chrissphere/todo.git
cd todo

# 启动服务
docker-compose up -d

# 访问应用
# 前端：http://localhost
# 后端 API：http://localhost:8000/api/v1
# API 文档：http://localhost:8000/docs
```

### 手动运行

**后端：**
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**前端：**
```bash
cd frontend
npm install
npm run dev
```

## 📖 文档

- [部署指南](DEPLOYMENT.md) - 本地开发、生产部署、云平台
- [API 文档](http://localhost:8000/docs) - Swagger/OpenAPI
- [数据库设计](docs/02-database-design.md)
- [开发任务](docs/03-development-tasks.md)

## 📁 项目结构

```
todo/
├── backend/              # FastAPI 后端
│   ├── app/
│   │   ├── api/         # API 端点
│   │   ├── models/      # 数据库模型
│   │   ├── schemas/     # Pydantic Schemas
│   │   ├── crud/        # CRUD 操作
│   │   └── core/        # 配置
│   ├── alembic/         # 数据库迁移
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/            # Vue3 前端
│   ├── src/
│   │   ├── api/        # API 请求
│   │   ├── views/      # 页面组件
│   │   ├── stores/     # Pinia stores
│   │   └── router/     # 路由
│   ├── Dockerfile
│   └── package.json
├── .github/workflows/   # GitHub Actions
├── docker-compose.yml   # Docker Compose 配置
├── DEPLOYMENT.md        # 部署文档
└── docs/                # 项目文档
```

## 🔧 开发

### 运行测试

```bash
# 后端
cd backend
pytest

# 前端
cd frontend
npm run test
```

### 代码规范

```bash
# 后端
flake8 app
black app

# 前端
npm run lint
npm run format
```

## 📦 Docker 镜像

- Backend: `chrissphere/todo-backend:latest`
- Frontend: `chrissphere/todo-frontend:latest`

```bash
docker pull chrissphere/todo-backend:latest
docker pull chrissphere/todo-frontend:latest
```

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📝 License

MIT License

## 👤 作者

Creed (chrissphere)

---

**Star ⭐ 这个项目如果对你有帮助！**
