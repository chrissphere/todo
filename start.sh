#!/bin/bash

# Todo App 快速启动脚本

set -e

echo "======================================"
echo "  Todo App - Docker Compose 启动"
echo "======================================"

# 检查 Docker 是否运行
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker 未运行，请先启动 Docker 服务"
    exit 1
fi

# 进入项目目录
cd "$(dirname "$0")"

# 检查配置文件
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ docker-compose.yml 不存在"
    exit 1
fi

echo "✅ 配置文件检查通过"

# 创建数据目录
mkdir -p data

# 启动服务
echo ""
echo "🚀 开始构建并启动服务..."
echo ""

docker-compose up -d --build

echo ""
echo "======================================"
echo "  服务启动完成！"
echo "======================================"
echo ""
echo "📱 访问地址："
echo "   前端：http://localhost"
echo "   后端 API：http://localhost:8000/api/v1"
echo "   API 文档：http://localhost:8000/docs"
echo ""
echo "🔧 常用命令："
echo "   查看日志：docker-compose logs -f"
echo "   停止服务：docker-compose down"
echo "   重启服务：docker-compose restart"
echo ""
echo "📊 查看状态："
docker-compose ps
echo ""
