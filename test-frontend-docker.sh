#!/bin/bash
# 测试前端 Docker 构建

echo "=========================================="
echo "前端 Docker 构建测试"
echo "=========================================="

cd /home/creed/hermes-agent/todo-app/frontend

echo ""
echo "1. 检查文件..."
ls -la package.json package-lock.json Dockerfile

echo ""
echo "2. 测试 npm install（模拟 Docker 环境）..."
rm -rf node_modules
npm ci --silent 2>&1 | tail -5

echo ""
echo "3. 测试 vite build..."
npx vite build 2>&1 | tail -20

echo ""
echo "4. 检查构建产物..."
ls -lh dist/

echo ""
echo "=========================================="
echo "测试完成"
echo "=========================================="
