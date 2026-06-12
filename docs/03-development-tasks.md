# 开发任务列表 (按优先级排序)

## 阶段 1: 后端基础架构 (P0)

### 1.1 项目初始化
- [x] 创建项目目录结构 (backend/, frontend/, docs/, docker/)
- [ ] 创建 backend/requirements.txt 文件
- [ ] 创建 backend/.env.example 文件
- [ ] 创建 backend/README.md 文件
- [ ] 初始化 Python 虚拟环境
- [ ] 安装 FastAPI 和 uvicorn
- [ ] 安装 SQLAlchemy 和 alembic
- [ ] 安装 pydantic 和 pydantic-settings
- [ ] 安装 pytest 和 pytest-asyncio

### 1.2 项目结构搭建
- [ ] 创建 backend/app/__init__.py
- [ ] 创建 backend/app/main.py (FastAPI 入口)
- [ ] 创建 backend/app/core/__init__.py
- [ ] 创建 backend/app/core/config.py (配置管理)
- [ ] 创建 backend/app/core/database.py (数据库连接)
- [ ] 创建 backend/app/models/__init__.py
- [ ] 创建 backend/app/schemas/__init__.py
- [ ] 创建 backend/app/api/__init__.py
- [ ] 创建 backend/app/crud/__init__.py

### 1.3 配置管理
- [ ] 定义 Settings 类 (pydantic-settings)
- [ ] 配置 DATABASE_URL
- [ ] 配置 CORS_ORIGINS
- [ ] 配置 PROJECT_NAME
- [ ] 创建 config 实例

### 1.4 数据库连接
- [ ] 创建 SQLAlchemy engine
- [ ] 创建 SessionLocal
- [ ] 创建 Base 元类
- [ ] 创建 get_db 依赖注入函数

### 1.5 Alembic 配置
- [ ] 初始化 alembic (alembic init alembic)
- [ ] 配置 alembic.ini (sqlalchemy.url)
- [ ] 配置 alembic/env.py (target_metadata)
- [ ] 创建第一个迁移 (initial_schema)
- [ ] 测试迁移 (alembic upgrade head)

## 阶段 2: 数据模型 (P0)

### 2.1 User 模型
- [ ] 创建 app/models/user.py
- [ ] 定义 User 模型类
- [ ] 定义字段：id, email, username, created_at
- [ ] 添加表名 __tablename__ = "users"
- [ ] 导出 User 模型

### 2.2 List 模型
- [ ] 创建 app/models/list.py
- [ ] 定义 List 模型类
- [ ] 定义字段：id, name, color, icon, sort_order, user_id
- [ ] 添加外键关系到 User
- [ ] 添加 relationship 到 Task
- [ ] 导出 List 模型

### 2.3 Tag 模型
- [ ] 创建 app/models/tag.py
- [ ] 定义 Tag 模型类
- [ ] 定义字段：id, name, color, user_id
- [ ] 添加唯一约束 (name, user_id)
- [ ] 添加 relationship 到 Task (secondary)
- [ ] 导出 Tag 模型

### 2.4 Task 模型
- [ ] 创建 app/models/task.py
- [ ] 定义 Task 模型类
- [ ] 定义基础字段：id, title, description, status, priority
- [ ] 定义日期字段：due_date, due_time, reminder_at
- [ ] 定义重复任务字段：is_recurring, recurring_rule
- [ ] 定义外键：parent_task_id, list_id, user_id
- [ ] 定义时间戳：created_at, updated_at, completed_at, deleted_at
- [ ] 添加外键约束
- [ ] 添加索引
- [ ] 导出 Task 模型

### 2.5 TaskTag 关联模型
- [ ] 创建 app/models/task_tag.py
- [ ] 定义 TaskTag 关联表
- [ ] 定义复合主键 (task_id, tag_id)
- [ ] 添加外键约束
- [ ] 导出 TaskTag 模型

### 2.6 模型关系完善
- [ ] 在 User 中添加 lists 和 tags 关系
- [ ] 在 List 中添加 tasks 关系
- [ ] 在 Task 中添加 parent/children 关系
- [ ] 在 Task 中添加 tags 关系 (many-to-many)
- [ ] 测试模型导入

## 阶段 3: Pydantic Schemas (P0)

### 3.1 Task Schemas
- [ ] 创建 app/schemas/task.py
- [ ] 定义 TaskBase (共享字段)
- [ ] 定义 TaskCreate (创建时的字段)
- [ ] 定义 TaskUpdate (更新时的字段，全部可选)
- [ ] 定义 TaskInDB (包含 ORM 模式)
- [ ] 定义 TaskResponse (API 响应)
- [ ] 定义 Priority 枚举
- [ ] 定义 TaskStatus 枚举

### 3.2 List Schemas
- [ ] 创建 app/schemas/list.py
- [ ] 定义 ListBase
- [ ] 定义 ListCreate
- [ ] 定义 ListUpdate
- [ ] 定义 ListResponse
- [ ] 定义 ListWithTasks (包含任务列表)

### 3.3 Tag Schemas
- [ ] 创建 app/schemas/tag.py
- [ ] 定义 TagBase
- [ ] 定义 TagCreate
- [ ] 定义 TagUpdate
- [ ] 定义 TagResponse

### 3.4 通用 Schemas
- [ ] 创建 app/schemas/base.py
- [ ] 定义 ResponseBase (通用响应包装)
- [ ] 定义 PaginationParams
- [ ] 定义 PaginatedResponse

## 阶段 4: CRUD 操作 (P0)

### 4.1 Base CRUD 类
- [ ] 创建 app/crud/base.py
- [ ] 定义 CRUDBase 泛型类
- [ ] 实现 get 方法
- [ ] 实现 get_multi 方法
- [ ] 实现 create 方法
- [ ] 实现 update 方法
- [ ] 实现 remove 方法

### 4.2 Task CRUD
- [ ] 创建 app/crud/task.py
- [ ] 实现 get 方法
- [ ] 实现 get_multi 方法 (支持过滤)
- [ ] 实现 create 方法
- [ ] 实现 update 方法
- [ ] 实现 remove 方法 (软删除)
- [ ] 实现 complete 方法
- [ ] 实现 get_by_list 方法
- [ ] 实现 search 方法

### 4.3 List CRUD
- [ ] 创建 app/crud/list.py
- [ ] 实现 get 方法
- [ ] 实现 get_multi 方法
- [ ] 实现 create 方法
- [ ] 实现 update 方法
- [ ] 实现 remove 方法
- [ ] 实现 get_by_user 方法

### 4.4 Tag CRUD
- [ ] 创建 app/crud/tag.py
- [ ] 实现 get 方法
- [ ] 实现 get_multi 方法
- [ ] 实现 create 方法
- [ ] 实现 update 方法
- [ ] 实现 remove 方法
- [ ] 实现 get_by_user 方法

## 阶段 5: API 路由 (P0)

### 5.1 API 基础结构
- [ ] 创建 app/api/deps.py (依赖注入)
- [ ] 创建 get_current_user 依赖 (临时返回 mock user)
- [ ] 创建 app/api/v1/__init__.py
- [ ] 创建 app/api/v1/router.py (APIRouter 集合)

### 5.2 Tasks API
- [ ] 创建 app/api/v1/endpoints/tasks.py
- [ ] 实现 GET /tasks (获取任务列表)
- [ ] 实现 GET /tasks/{task_id} (获取单个任务)
- [ ] 实现 POST /tasks (创建任务)
- [ ] 实现 PUT /tasks/{task_id} (更新任务)
- [ ] 实现 DELETE /tasks/{task_id} (删除任务)
- [ ] 实现 PATCH /tasks/{task_id}/complete (完成任务)
- [ ] 实现 GET /lists/{list_id}/tasks (获取清单下的任务)

### 5.3 Lists API
- [ ] 创建 app/api/v1/endpoints/lists.py
- [ ] 实现 GET /lists (获取清单列表)
- [ ] 实现 GET /lists/{list_id} (获取单个清单)
- [ ] 实现 POST /lists (创建清单)
- [ ] 实现 PUT /lists/{list_id} (更新清单)
- [ ] 实现 DELETE /lists/{list_id} (删除清单)

### 5.4 Tags API
- [ ] 创建 app/api/v1/endpoints/tags.py
- [ ] 实现 GET /tags (获取标签列表)
- [ ] 实现 GET /tags/{tag_id} (获取单个标签)
- [ ] 实现 POST /tags (创建标签)
- [ ] 实现 PUT /tags/{tag_id} (更新标签)
- [ ] 实现 DELETE /tags/{tag_id} (删除标签)

### 5.5 API 路由注册
- [ ] 在 router.py 中注册 tasks 路由
- [ ] 在 router.py 中注册 lists 路由
- [ ] 在 router.py 中注册 tags 路由
- [ ] 在 main.py 中包含 router
- [ ] 测试 API 端点

## 阶段 6: 高级功能 (P1)

### 6.1 子任务功能
- [ ] 在 Task schema 中添加 children 字段
- [ ] 实现 GET /tasks/{task_id}/subtasks
- [ ] 实现 POST /tasks/{task_id}/subtasks
- [ ] 实现子任务进度计算

### 6.2 任务标签关联
- [ ] 实现 POST /tasks/{task_id}/tags/{tag_id} (添加标签)
- [ ] 实现 DELETE /tasks/{task_id}/tags/{tag_id} (移除标签)
- [ ] 实现 GET /tags/{tag_id}/tasks (获取标签下的任务)

### 6.3 搜索和过滤
- [ ] 实现 GET /tasks/search?q= (全文搜索)
- [ ] 实现 GET /tasks/filter?priority=high&status=pending
- [ ] 实现 GET /tasks/today (今天的任务)
- [ ] 实现 GET /tasks/overdue (过期的任务)

### 6.4 重复任务逻辑
- [ ] 创建 app/services/recurring.py
- [ ] 实现 parse_recurring_rule 函数
- [ ] 实现 calculate_next_occurrence 函数
- [ ] 实现 complete_and_reschedule 函数

## 阶段 7: 前端基础 (P0)

### 7.1 项目初始化
- [ ] 创建 frontend/ 目录
- [ ] 创建 frontend/package.json
- [ ] 创建 frontend/vite.config.js
- [ ] 创建 frontend/index.html
- [ ] 创建 frontend/src/main.js
- [ ] 创建 frontend/src/App.vue
- [ ] 安装 Vue 3
- [ ] 安装 Element Plus
- [ ] 安装 axios
- [ ] 安装 pinia (状态管理)
- [ ] 安装 vue-router

### 7.2 项目结构
- [ ] 创建 frontend/src/api/ (API 调用)
- [ ] 创建 frontend/src/components/ (通用组件)
- [ ] 创建 frontend/src/views/ (页面组件)
- [ ] 创建 frontend/src/stores/ (Pinia stores)
- [ ] 创建 frontend/src/router/ (路由配置)
- [ ] 创建 frontend/src/styles/ (样式文件)
- [ ] 创建 frontend/src/utils/ (工具函数)

### 7.3 API 客户端
- [ ] 创建 frontend/src/api/client.js (axios 实例)
- [ ] 配置 baseURL
- [ ] 配置请求拦截器
- [ ] 配置响应拦截器
- [ ] 创建 frontend/src/api/tasks.js
- [ ] 创建 frontend/src/api/lists.js
- [ ] 创建 frontend/src/api/tags.js

### 7.4 状态管理
- [ ] 创建 frontend/src/stores/task.js
- [ ] 定义 task state
- [ ] 定义 task actions (fetch, create, update, delete)
- [ ] 创建 frontend/src/stores/list.js
- [ ] 创建 frontend/src/stores/tag.js

### 7.5 路由配置
- [ ] 创建 frontend/src/router/index.js
- [ ] 配置 / 路由 (主页)
- [ ] 配置 /tasks/:id 路由 (任务详情)
- [ ] 配置 /lists/:id 路由 (清单视图)
- [ ] 配置 /tags/:id 路由 (标签视图)

## 阶段 8: 前端组件 (P0)

### 8.1 布局组件
- [ ] 创建 frontend/src/components/Layout.vue
- [ ] 创建侧边栏组件 Sidebar.vue
- [ ] 创建顶部导航 Header.vue
- [ ] 创建主内容区 MainContent.vue

### 8.2 任务组件
- [ ] 创建 TaskItem.vue (任务列表项)
- [ ] 创建 TaskList.vue (任务列表容器)
- [ ] 创建 TaskForm.vue (任务表单)
- [ ] 创建 TaskDetail.vue (任务详情)
- [ ] 创建 PriorityIcon.vue (优先级图标)
- [ ] 创建 DueDateBadge.vue (截止日期标签)

### 8.3 清单组件
- [ ] 创建 ListItem.vue (清单项)
- [ ] 创建 ListSelector.vue (清单选择器)
- [ ] 创建 ListForm.vue (清单表单)

### 8.4 通用组件
- [ ] 创建 SearchBar.vue (搜索框)
- [ ] 创建 FilterBar.vue (过滤栏)
- [ ] 创建 Pagination.vue (分页组件)
- [ ] 创建 LoadingSpinner.vue (加载动画)
- [ ] 创建 EmptyState.vue (空状态)

## 阶段 9: 前端页面 (P0)

### 9.1 主页
- [ ] 创建 frontend/src/views/Home.vue
- [ ] 实现侧边栏布局
- [ ] 实现任务列表展示
- [ ] 实现快速添加任务
- [ ] 实现任务完成切换

### 9.2 清单页面
- [ ] 创建 frontend/src/views/ListDetail.vue
- [ ] 实现清单任务筛选
- [ ] 实现清单信息编辑

### 9.3 标签页面
- [ ] 创建 frontend/src/views/TagDetail.vue
- [ ] 实现标签任务筛选

### 9.4 搜索页面
- [ ] 创建 frontend/src/views/Search.vue
- [ ] 实现搜索结果展示
- [ ] 实现高级筛选表单

## 阶段 10: 样式和主题 (P1)

### 10.1 主题配置
- [ ] 创建 frontend/src/styles/variables.css
- [ ] 定义颜色变量
- [ ] 定义间距变量
- [ ] 定义字体变量

### 10.2 优先级样式
- [ ] 定义高优先级颜色 (红色)
- [ ] 定义中优先级颜色 (黄色)
- [ ] 定义低优先级颜色 (蓝色)
- [ ] 定义无优先级颜色 (灰色)

### 10.3 响应式设计
- [ ] 添加移动端媒体查询
- [ ] 优化侧边栏折叠
- [ ] 优化任务列表布局

## 阶段 11: Docker 配置 (P1)

### 11.1 Dockerfile
- [ ] 创建 backend/Dockerfile
- [ ] 配置 Python 基础镜像
- [ ] 安装依赖
- [ ] 复制代码
- [ ] 暴露端口
- [ ] 创建 frontend/Dockerfile
- [ ] 配置 Node 基础镜像
- [ ] 构建前端应用
- [ ] 使用 nginx 服务静态文件

### 11.2 Docker Compose
- [ ] 创建 docker-compose.yml
- [ ] 定义 backend 服务
- [ ] 定义 frontend 服务
- [ ] 定义网络
- [ ] 定义卷挂载

### 11.3 Nginx 配置
- [ ] 创建 docker/nginx/nginx.conf
- [ ] 配置反向代理
- [ ] 配置静态文件服务
- [ ] 配置 API 转发

## 阶段 12: 测试和文档 (P2)

### 12.1 后端测试
- [ ] 创建 backend/tests/__init__.py
- [ ] 创建 backend/tests/conftest.py (pytest fixtures)
- [ ] 创建 backend/tests/test_tasks.py
- [ ] 创建 backend/tests/test_lists.py
- [ ] 创建 backend/tests/test_tags.py
- [ ] 运行测试并修复

### 12.2 API 文档
- [ ] 完善 API docstrings
- [ ] 配置 Swagger UI
- [ ] 测试 API 文档

### 12.3 项目文档
- [ ] 创建 README.md
- [ ] 编写安装指南
- [ ] 编写使用指南
- [ ] 编写 API 文档

---

## 任务统计

- **总任务数**: 约 200+ 个
- **P0 (MVP)**: 约 100 个任务
- **P1 (核心体验)**: 约 70 个任务
- **P2 (增强功能)**: 约 30 个任务
- **平均任务时间**: 2-5 分钟
- **预计总开发时间**: 10-15 小时 (按顺序执行)

## 开发建议

1. **按阶段顺序开发**: 每个阶段的任务有依赖关系
2. **小步快跑**: 每完成 5-10 个小任务就测试一次
3. **优先 P0**: 先完成 MVP，再迭代增强功能
4. **及时提交**: 每个小功能完成后立即 git commit
5. **文档同步**: 开发过程中同步更新文档
