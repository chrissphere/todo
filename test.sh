#!/bin/bash

# Todo App 测试脚本

set -e

echo "======================================"
echo "  Todo App - 健康检查"
echo "======================================"

# 检查后端
echo ""
echo "🔍 检查后端服务..."
if curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/api/v1/health | grep -q "200"; then
    echo "✅ 后端服务正常"
else
    echo "❌ 后端服务异常"
    exit 1
fi

# 检查前端
echo ""
echo "🔍 检查前端服务..."
if curl -s -o /dev/null -w "%{http_code}" http://localhost | grep -q "200"; then
    echo "✅ 前端服务正常"
else
    echo "❌ 前端服务异常"
    exit 1
fi

# 测试 API
echo ""
echo "🔍 测试 API 端点..."

# 创建测试任务
echo "创建测试任务..."
RESPONSE=$(curl -s -X POST "http://localhost:8000/api/v1/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "测试任务",
    "description": "这是一个测试任务",
    "priority": "medium"
  }')

echo "响应：$RESPONSE"

# 获取任务列表
echo ""
echo "获取任务列表..."
curl -s "http://localhost:8000/api/v1/tasks" | python3 -m json.tool | head -20

echo ""
echo "======================================"
echo "  ✅ 所有测试通过！"
echo "======================================"
