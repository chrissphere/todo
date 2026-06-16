# Docker 配置验证报告

## ✅ 配置检查清单

### 1. Docker 文件配置

| 文件 | 状态 | 说明 |
|------|------|------|
| `backend/Dockerfile` | ✅ 正确 | Python 3.11-slim, uvicorn 启动 |
| `frontend/Dockerfile` | ✅ 正确 | Node 20 构建 + Nginx alpine |
| `frontend/nginx.conf` | ✅ 正确 | Vue Router history 模式支持 |
| `docker-compose.yml` | ✅ 正确 | 服务编排 + 健康检查 |
| `backend/.dockerignore` | ✅ 正确 | 排除缓存和虚拟环境 |
| `frontend/.dockerignore` | ✅ 正确 | 排除 node_modules |

### 2. GitHub Actions Workflows

| Workflow | 状态 | 功能 |
|----------|------|------|
| `.github/workflows/ci.yml` | ✅ 正确 | 前后端 lint + test + build |
| `.github/workflows/docker-build.yml` | ✅ 正确 | 构建→测试→推送→部署 |

### 3. 运维脚本

| 脚本 | 状态 | 权限 | 功能 |
|------|------|------|------|
| `start.sh` | ✅ 正确 | 755 | 启动所有服务 |
| `init_db.sh` | ✅ 正确 | 755 | 初始化数据库 |
| `test.sh` | ✅ 正确 | 755 | 健康检查 + API 测试 |
| `stop.sh` | ✅ 正确 | 755 | 停止所有服务 |

---

## 🚀 本地部署步骤

### 前提条件

1. **安装 Docker 和 Docker Compose**

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y docker.io docker-compose

# 验证安装
docker --version
docker-compose --version
```

2. **配置 Docker 镜像源（中国大陆推荐）**

```bash
sudo mkdir -p /etc/docker
sudo tee /etc/docker/daemon.json <<-'EOF'
{
  "registry-mirrors": [
    "https://docker.m.daocloud.io",
    "https://registry.cn-hangzhou.aliyuncs.com"
  ]
}
EOF
sudo systemctl restart docker
```

3. **添加用户到 docker 组（可选）**

```bash
sudo usermod -aG docker $USER
newgrp docker
```

### 启动服务

```bash
cd /home/creed/hermes-agent/todo-app

# 方式 1：使用脚本（推荐）
./start.sh

# 方式 2：直接使用 docker-compose
docker-compose up -d --build
```

### 验证服务

```bash
# 查看容器状态
docker-compose ps

# 查看日志
docker-compose logs -f

# 运行健康检查
./test.sh
```

### 访问应用

- **前端**: http://localhost
- **后端 API**: http://localhost:8000/api/v1
- **API 文档**: http://localhost:8000/docs
- **Swagger UI**: http://localhost:8000/redoc

### 停止服务

```bash
# 方式 1：使用脚本
./stop.sh

# 方式 2：直接使用 docker-compose
docker-compose down

# 删除数据卷（谨慎使用）
docker-compose down -v
```

---

## 🔧 GitHub Actions 配置

### 1. 配置 Docker Hub Secrets

在 GitHub 仓库中：

```
Settings → Secrets and variables → Actions → New repository secret

添加以下 secrets：
- DOCKER_USERNAME: 你的 Docker Hub 用户名
- DOCKER_TOKEN: Docker Hub Access Token
```

**获取 Docker Token：**
1. 访问 https://hub.docker.com/settings/security
2. 点击 "Generate Access Token"
3. 输入描述（如 "GitHub Actions"）
4. 选择权限（Read & Write）
5. 生成并复制 token

### 2. 触发自动构建

```bash
# 推送到 main 分支触发构建和推送
git push origin main

# 或者创建 tag 触发版本构建
git tag v1.0.0
git push origin v1.0.0
```

### 3. 查看构建状态

- **Actions 标签页**: https://github.com/chrissphere/todo/actions
- **镜像仓库**: https://hub.docker.com/r/chrissphere/todo-backend

---

## 📊 预期输出

### 启动成功输出

```
✅ 配置文件检查通过

🚀 开始构建并启动服务...

Creating network "todo-app_default" with the default driver
Creating volume "todo-app_data" with default driver
Building backend
Step 1/10 : FROM python:3.11-slim
...
Building frontend
Step 1/7 : FROM node:20-alpine
...
Creating todo-backend ... done
Creating todo-frontend ... done

======================================
  服务启动完成！
======================================

📱 访问地址：
   前端：http://localhost
   后端 API：http://localhost:8000/api/v1
   API 文档：http://localhost:8000/docs

📊 查看状态：
   NAME             STATUS         PORTS
   todo-backend     Up (healthy)   0.0.0.0:8000->8000/tcp
   todo-frontend    Up             0.0.0.0:80->80/tcp
```

### 健康检查输出

```
======================================
  Todo App - 健康检查
======================================

🔍 检查后端服务...
✅ 后端服务正常

🔍 检查前端服务...
✅ 前端服务正常

🔍 测试 API 端点...
创建测试任务...
响应：{"id":1,"title":"测试任务",...}

获取任务列表...
[
  {
    "id": 1,
    "title": "测试任务",
    "description": "这是一个测试任务",
    "priority": "medium",
    ...
  }
]

======================================
  ✅ 所有测试通过！
======================================
```

---

## ⚠️ 常见问题

### 1. Docker 构建超时

**问题**: `failed to resolve reference` 或构建超时

**解决**:
```bash
# 配置国内镜像源
sudo tee /etc/docker/daemon.json <<-'EOF'
{
  "registry-mirrors": [
    "https://docker.m.daocloud.io",
    "https://registry.cn-hangzhou.aliyuncs.com"
  ]
}
EOF
sudo systemctl restart docker
```

### 2. 端口冲突

**问题**: `Bind for 0.0.0.0:80 failed: port is already allocated`

**解决**:
```bash
# 修改 docker-compose.yml 中的端口映射
ports:
  - "8080:80"  # 前端改为 8080
  - "8001:8000"  # 后端改为 8001
```

### 3. 权限问题

**问题**: `permission denied while trying to connect to the docker daemon`

**解决**:
```bash
# 添加用户到 docker 组
sudo usermod -aG docker $USER
newgrp docker

# 或者使用 sudo
sudo docker-compose up -d
```

### 4. 数据库文件不存在

**问题**: 容器启动但数据库未初始化

**解决**:
```bash
# 手动初始化数据库
./init_db.sh

# 或者进入容器执行
docker-compose exec backend python init_db.py
```

### 5. 前端无法访问后端 API

**问题**: 前端请求后端 API 返回 404 或 CORS 错误

**解决**:
- 确认 nginx.conf 中配置了 API 代理
- 检查后端 CORS 配置
- 确认后端服务正常运行：`docker-compose logs backend`

---

## 📈 性能优化建议

### 1. 启用 Buildx 缓存

```yaml
# .github/workflows/docker-build.yml
- name: Build and push
  uses: docker/build-push-action@v5
  with:
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

### 2. 多阶段构建减少镜像大小

```dockerfile
# frontend/Dockerfile 已使用多阶段构建
FROM node:20-alpine AS builder
...
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
```

### 3. 使用 .dockerignore 减少上下文

```bash
# 已配置 .dockerignore 文件
# 排除 node_modules, __pycache__, .git 等
```

---

## ✅ 验证清单

- [ ] Docker 和 Docker Compose 已安装
- [ ] 镜像源已配置（中国大陆）
- [ ] `docker-compose up -d --build` 成功
- [ ] 前端可以访问（http://localhost）
- [ ] 后端 API 可以访问（http://localhost:8000/api/v1）
- [ ] API 文档正常显示（http://localhost:8000/docs）
- [ ] 健康检查脚本通过（`./test.sh`）
- [ ] GitHub Secrets 已配置
- [ ] GitHub Actions 触发成功
- [ ] Docker Hub 镜像推送成功

---

**生成时间**: 2026-06-16
**项目版本**: v1.0.0
**作者**: Creed (chrissphere)
