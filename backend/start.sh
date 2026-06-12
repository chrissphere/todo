#!/bin/bash
# Todo App 后端快速启动脚本

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "========================================"
echo "  Todo App Backend - 快速启动"
echo "========================================"
echo ""

# 检查虚拟环境
if [ ! -d ".venv" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv .venv
fi

# 激活虚拟环境
echo "🔌 激活虚拟环境..."
source .venv/bin/activate

# 安装依赖
echo "📥 安装依赖..."
pip install -q -r requirements.txt

# 初始化数据库
echo "🗄️  初始化数据库..."
python init_db.py

# 启动服务器
echo ""
echo "🚀 启动服务器..."
echo "========================================"
echo "API 文档：http://localhost:8000/api/v1/docs"
echo "ReDoc:    http://localhost:8000/api/v1/redoc"
echo "========================================"
echo ""

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
