#!/bin/bash

# Todo App 停止脚本

set -e

echo "======================================"
echo "  Todo App - 停止服务"
echo "======================================"

cd "$(dirname "$0")"

echo "🛑 停止所有服务..."
docker-compose down

echo ""
echo "✅ 服务已停止"
echo ""
echo "💡 提示："
echo "   删除数据卷：docker-compose down -v"
echo "   删除镜像：docker-compose down --rmi all"
echo ""
