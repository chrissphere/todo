# Todo App Frontend

待办事项系统前端 - Vue3 + TypeScript + Element Plus

## 技术栈

- **框架**: Vue 3.4 + TypeScript
- **构建工具**: Vite 5
- **UI 组件库**: Element Plus
- **状态管理**: Pinia
- **路由**: Vue Router 4
- **HTTP 客户端**: Axios
- **代码规范**: ESLint + Prettier

## 功能

- ✅ 任务管理（创建、编辑、删除、完成）
- ✅ 清单/列表管理
- ✅ 优先级设置（高、中、低）
- ✅ 截止日期和提醒时间
- ✅ 任务过滤（未完成/已完成/全部）
- ✅ 响应式布局

## 快速开始

### 安装依赖

```bash
npm install
# 或
pnpm install
# 或
yarn install
```

### 开发模式

```bash
npm run dev
```

访问 http://localhost:3000

### 构建生产版本

```bash
npm run build
```

### 代码检查

```bash
npm run lint
npm run format
```

## 项目结构

```
frontend/
├── src/
│   ├── api/           # API 请求封装
│   ├── assets/        # 静态资源
│   ├── components/    # 通用组件
│   ├── router/        # 路由配置
│   ├── stores/        # Pinia stores
│   ├── types/         # TypeScript 类型定义
│   ├── utils/         # 工具函数
│   ├── views/         # 页面组件
│   ├── App.vue        # 根组件
│   └── main.ts        # 入口文件
├── index.html
├── package.json
├── tsconfig.json
├── vite.config.ts
└── ...
```

## API 配置

开发模式下，API 请求会代理到后端服务 (http://localhost:8000)

在 `vite.config.ts` 中配置代理：

```typescript
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true
    }
  }
}
```

## License

MIT
