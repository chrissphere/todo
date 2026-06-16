# 部署指南

## 本地开发

### 使用 Docker Compose（推荐）

```bash
# 启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down

# 重建并启动
docker-compose up -d --build
```

访问：
- 前端：http://localhost
- 后端 API：http://localhost:8000/api/v1
- API 文档：http://localhost:8000/docs

### 手动运行

**后端：**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**前端：**
```bash
cd frontend
npm install
npm run dev
```

---

## 生产环境部署

### 方案 1：Docker Compose（单机部署）

1. **准备服务器**
   - Ubuntu 20.04+ / Debian 11+
   - 安装 Docker 和 Docker Compose
   - 开放端口 80 (前端) 和 8000 (后端 API)

2. **配置环境变量（可选）**

创建 `.env` 文件：
```bash
# 数据库
DATABASE_URL=postgresql://user:password@localhost:5432/todo

# 安全
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

3. **部署**

```bash
# 克隆仓库
git clone https://github.com/chrissphere/todo.git
cd todo

# 启动服务
docker-compose up -d

# 查看状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

4. **配置域名（可选）**

使用 Nginx 反向代理：
```nginx
server {
    listen 80;
    server_name todo.yourdomain.com;

    location / {
        proxy_pass http://localhost:80;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

### 方案 2：GitHub Actions 自动部署

1. **无需配置 Secrets**

使用 GitHub Container Registry (GHCR) 不需要额外配置 secrets，GitHub 会自动使用 `GITHUB_TOKEN`。

2. **自动构建和推送**

每次 push 到 main 分支会自动：
- 构建前后端 Docker 镜像
- 推送到 GitHub Container Registry (GHCR)
- 标签格式：
  - `ghcr.io/chrissphere/todo-backend:main`
  - `ghcr.io/chrissphere/todo-backend:sha-abc123`
  - `ghcr.io/chrissphere/todo-frontend:main`
  - `ghcr.io/chrissphere/todo-frontend:sha-abc123`

3. **自动部署（需要配置 SSH）**

编辑 `.github/workflows/docker-build.yml`，启用 deploy job 中的 SSH 步骤。

---

### 方案 3：云平台部署

#### GHCR + Railway/Render/Fly.io

1. 推送镜像到 GHCR（CI 自动完成）
2. 在云平台创建应用，指定镜像：
   - Backend: `ghcr.io/chrissphere/todo-backend:main`
   - Frontend: `ghcr.io/chrissphere/todo-frontend:main`
3. 配置环境变量和数据库连接

注意：部分云平台需要从 GHCR 拉取镜像的权限，可能需要配置 Docker Hub 镜像同步。

#### Kubernetes

创建 `k8s/` 目录，添加：
- `deployment.yaml` - 定义前后端 Deployment
- `service.yaml` - 定义 Service 和 Ingress
- `configmap.yaml` - 配置环境变量

```bash
kubectl apply -f k8s/
```

---

## 数据库迁移

首次部署时运行数据库初始化：

```bash
docker-compose exec backend python init_db.py
```

或使用 Alembic：
```bash
docker-compose exec backend alembic upgrade head
```

---

## 监控和日志

### 查看日志
```bash
# 所有服务
docker-compose logs -f

# 单个服务
docker-compose logs -f backend
docker-compose logs -f frontend
```

### 健康检查
```bash
# 后端健康检查
curl http://localhost:8000/api/v1/health

# 前端
curl http://localhost
```

---

## 备份和恢复

### 备份数据库
```bash
# SQLite
docker cp todo-backend:/app/data/todo.db ./backup-$(date +%Y%m%d).db

# PostgreSQL
docker exec todo-postgres pg_dump -U user todo > backup.sql
```

### 恢复数据库
```bash
# SQLite
docker cp backup.db todo-backend:/app/data/todo.db

# PostgreSQL
cat backup.sql | docker exec -i todo-postgres psql -U user -d todo
```

---

## 故障排查

### 常见问题

1. **容器启动失败**
   ```bash
   docker-compose logs backend
   docker-compose logs frontend
   ```

2. **端口冲突**
   ```bash
   # 修改 docker-compose.yml 中的端口映射
   ports:
     - "8080:80"  # 前端改为 8080
     - "8001:8000"  # 后端改为 8001
   ```

3. **数据库连接失败**
   - 检查 `DATABASE_URL` 环境变量
   - 确保数据库服务已启动
   - 检查网络连接

4. **前端无法访问后端 API**
   - 检查 nginx.conf 中的 proxy_pass 配置
   - 确认后端服务正常运行
   - 检查 CORS 配置

---

## 性能优化

1. **启用 Redis 缓存**
2. **使用 PostgreSQL 替代 SQLite**
3. **配置 CDN 加速静态资源**
4. **启用 Gzip 压缩**
5. **配置数据库连接池**

---

## 安全建议

1. **修改默认密钥**
   - 生成新的 `SECRET_KEY`
   - 使用强密码保护数据库

2. **启用 HTTPS**
   - 使用 Let's Encrypt 免费证书
   - 配置 Traefik 或 Nginx

3. **限制 API 访问**
   - 配置防火墙规则
   - 使用速率限制

4. **定期更新依赖**
   ```bash
   # 后端
   pip review --auto
   
   # 前端
   npm audit fix
   ```
