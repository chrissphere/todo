#!/bin/bash

# 数据库初始化脚本

set -e

echo "🔧 初始化数据库..."

# 等待后端服务启动
echo "等待后端服务就绪..."
sleep 5

# 执行数据库初始化
docker-compose exec -T backend python -c "
from app.database.init_db import init_db
init_db()
print('✅ 数据库初始化完成')
"

echo ""
echo "✅ 数据库初始化完成！"
