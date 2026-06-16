# GitHub Actions 自动构建指南

## ✅ 配置完成

你的项目已配置使用 **GitHub Container Registry (GHCR)**，无需额外 secrets！

---

## 🚀 触发自动构建

### 方式 1：推送到 main 分支

```bash
git push origin main
```

### 方式 2：创建版本标签

```bash
git tag v1.0.0
git push origin v1.0.0
```

### 方式 3：创建 Pull Request

```bash
git checkout -b feature/new-feature
git push origin feature/new-feature
# 然后在 GitHub 上创建 PR
```

---

## 📦 镜像地址

构建成功后，镜像会自动推送到：

### 后端镜像
- **Main 分支**: `ghcr.io/chrissphere/todo-backend:main`
- **版本标签**: `ghcr.io/chrissphere/todo-backend:v1.0.0`
- **Commit SHA**: `ghcr.io/chrissphere/todo-backend:sha-6d84d55`

### 前端镜像
- **Main 分支**: `ghcr.io/chrissphere/todo-frontend:main`
- **版本标签**: `ghcr.io/chrissphere/todo-frontend:v1.0.0`
- **Commit SHA**: `ghcr.io/chrissphere/todo-frontend:sha-6d84d55`

---

## 🔍 查看构建状态

### 1. GitHub Actions 页面

访问：https://github.com/chrissphere/todo/actions

你会看到：
- ✅ CI - 代码检查和测试
- ✅ Docker Build and Push - 构建和推送镜像

### 2. 查看构建日志

点击对应的 workflow → 查看每个 job 的详细日志

### 3. 查看已推送的镜像

访问：https://github.com/chrissphere/todo/pkgs/container/todo-backend

或者使用命令行：
```bash
# 需要登录 GitHub
docker login ghcr.io -u chrissphere
docker pull ghcr.io/chrissphere/todo-backend:main
```

---

## 📊 构建流程

```
push 到 main 分支
    ↓
触发 GitHub Actions
    ↓
┌─────────────────────┐
│  build-backend      │  ← 构建后端镜像
│  - checkout         │
│  - setup buildx     │
│  - docker build     │
│  - run pytest       │
└─────────────────────┘
    ↓
┌─────────────────────┐
│  build-frontend     │  ← 构建前端镜像
│  - checkout         │
│  - setup buildx     │
│  - docker build     │
│  - nginx test       │
└─────────────────────┘
    ↓
┌─────────────────────┐
│  push-images        │  ← 推送镜像到 GHCR
│  - login to GHCR    │
│  - docker push      │
│  - multi-arch       │
└─────────────────────┘
    ↓
✅ 完成！镜像已推送到 ghcr.io
```

---

## 🔐 权限配置

### GHCR 镜像可见性

默认情况下，GHCR 镜像的可见性与仓库一致：

- **公开仓库** → 公开镜像（任何人都可以拉取）
- **私有仓库** → 私有镜像（需要认证才能拉取）

### 修改镜像可见性

如果需要修改：

1. 访问：https://github.com/chrissphere/todo/pkgs/container/todo-backend
2. 点击右上角 ⚙️ (Package settings)
3. 滚动到 "Danger Zone"
4. 点击 "Change visibility"

---

## 🌍 拉取镜像

### 公开镜像（无需认证）

```bash
docker pull ghcr.io/chrissphere/todo-backend:main
docker pull ghcr.io/chrissphere/todo-frontend:main
```

### 私有镜像（需要认证）

```bash
# 登录 GHCR
echo $GITHUB_TOKEN | docker login ghcr.io -u chrissphere --password-stdin

# 拉取镜像
docker pull ghcr.io/chrissphere/todo-backend:main
```

**获取 GITHUB_TOKEN：**
https://github.com/settings/tokens → Generate new token (classic)
- 权限：`read:packages`

---

## 📈 构建优化

### 1. 启用缓存

Workflow 已配置 GitHub Actions 缓存：
```yaml
cache-from: type=gha
cache-to: type=gha,mode=max
```

后续构建会更快！

### 2. 多架构构建（可选）

如果需要支持 ARM64（如 Raspberry Pi, M1 Mac）：

编辑 `.github/workflows/docker-build.yml`：
```yaml
- name: Build and push backend
  uses: docker/build-push-action@v5
  with:
    platforms: linux/amd64,linux/arm64
    # ...其他配置
```

---

## ⚠️ 常见问题

### Q1: 构建失败怎么办？

**A:** 
1. 查看 Actions 日志，找到具体错误
2. 常见错误：
   - Dockerfile 语法错误
   - 依赖安装失败
   - 测试未通过

### Q2: 如何重新运行失败的构建？

**A:** 
在 Actions 页面点击 "Re-run jobs" 按钮

### Q3: 如何取消正在运行的构建？

**A:** 
在 Actions 页面点击 "Cancel workflow" 按钮

### Q4: 镜像推送失败？

**A:** 
检查：
- 仓库是否有 packages 权限
- GITHUB_TOKEN 是否有效
- 镜像名称是否正确

### Q5: 国内访问 GHCR 慢？

**A:** 
GHCR 国内访问速度比 Docker Hub 快，但如果仍然慢：
- 使用国内镜像代理
- 或在服务器上配置代理

---

## 🎯 下一步

1. **触发第一次构建**：
   ```bash
   git push origin main
   ```

2. **监控构建进度**：
   访问 https://github.com/chrissphere/todo/actions

3. **验证镜像推送**：
   构建完成后访问 https://github.com/chrissphere/todo/pkgs

4. **部署到服务器**：
   ```bash
   # 在服务器上拉取镜像
   docker pull ghcr.io/chrissphere/todo-backend:main
   docker pull ghcr.io/chrissphere/todo-frontend:main
   
   # 使用 docker-compose 启动
   docker-compose up -d
   ```

---

**生成时间**: 2026-06-16
**项目**: Todo App
**作者**: Creed (chrissphere)
