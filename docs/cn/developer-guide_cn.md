# 开发指南

## 快速开始

### 环境准备
1. Node.js >= 16
2. Python >= 3.8
3. Git

### 克隆项目
```bash
git clone <repository-url>
cd c2
```

### 前端开发
```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

### 后端开发
```bash
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
.\venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑.env文件，填入必要的配置

# 启动开发服务器
python run.py
```

## 项目结构说明

### 前端结构
```
frontend/
├── src/                # 源代码目录
│   ├── api.ts         # API 接口封装
│   ├── App.vue        # 根组件
│   ├── main.ts        # 入口文件
│   ├── router/        # 路由配置
│   └── views/         # 页面组件
├── public/            # 静态资源
└── vite.config.ts     # Vite 配置
```

### 后端结构
```
backend/
├── src/              # 源代码目录
│   ├── api/         # API 相关代码
│   │   ├── models/  # 数据模型
│   │   └── routers/ # 路由处理
│   ├── config/      # 配置文件
│   └── core/        # 核心功能
├── tests/           # 测试代码
└── run.py           # 入口文件
```

## 开发规范

### 代码风格
- 前端遵循 TypeScript 标准规范
- 后端遵循 PEP 8 规范
- 使用 ESLint 和 Prettier 进行代码格式化
- 使用 Python Black 格式化 Python 代码

### Git 提交规范
```
feat: 新功能
fix: 修复bug
docs: 文档更新
style: 代码格式（不影响代码运行的变动）
refactor: 重构（既不是新增功能，也不是修改bug的代码变动）
perf: 性能优化
test: 增加测试
chore: 构建过程或辅助工具的变动
```

### 分支管理
- main: 主分支，用于生产环境
- develop: 开发分支，用于开发环境
- feature/*: 功能分支
- hotfix/*: 紧急修复分支

## 开发流程

### 1. 功能开发
1. 从 develop 分支创建功能分支
   ```bash
   git checkout develop
   git checkout -b feature/your-feature
   ```

2. 开发新功能
   - 编写代码
   - 编写测试
   - 本地测试

3. 提交代码
   ```bash
   git add .
   git commit -m "feat: your feature description"
   ```

4. 推送到远程
   ```bash
   git push origin feature/your-feature
   ```

5. 创建 Pull Request

### 2. 代码审查
- 检查代码规范
- 运行测试用例
- 代码评审
- 处理反馈意见

### 3. 合并代码
- 合并到 develop 分支
- 删除功能分支

## 测试指南

### 单元测试
- 前端使用 Jest 进行单元测试
  ```bash
  cd frontend
  npm run test:unit
  ```

- 后端使用 pytest 进行单元测试
  ```bash
  cd backend
  python -m pytest tests/
  ```

### 端到端测试
- 使用 Cypress 进行 E2E 测试
  ```bash
  cd frontend
  npm run test:e2e
  ```

## 调试技巧

### 前端调试
1. Vue Devtools
   - 安装 Vue.js devtools 浏览器插件
   - 使用开发者工具查看组件状态

2. 网络调试
   - 使用浏览器开发者工具的 Network 面板
   - 监控 API 请求和响应

3. 代码调试
   - 使用 console.log() 输出信息
   - 使用 debugger 设置断点
   - 使用 VSCode 调试配置

### 后端调试
1. 日志调试
   ```python
   import logging
   logging.debug("Debug message")
   ```

2. 使用 pdb
   ```python
   import pdb; pdb.set_trace()
   ```

3. 使用 VSCode 调试配置
   - 配置 launch.json
   - 设置断点
   - 使用调试控制台

## 常见问题

### 1. 环境配置问题
- 检查 Node.js 版本
- 检查 Python 版本
- 确认所有依赖已安装
- 验证环境变量配置

### 2. API 调用问题
- 检查 API 地址配置
- 确认请求方法和参数
- 查看网络请求日志
- 验证认证信息

### 3. 数据库连接问题
- 检查数据库配置
- 确认数据库服务运行状态
- 验证连接字符串
- 检查用户权限

## 部署说明

### 开发环境
- 本地开发服务器
- 本地数据库
- 模拟第三方服务

### 测试环境
- 独立测试服务器
- 测试数据库
- 测试第三方服务

### 生产环境
- 使用 Docker 容器化部署
- 使用 Nginx 作为反向代理
- 使用 PM2 管理 Node.js 进程
- 使用 Gunicorn 运行 Python 应用

## 性能优化

### 前端优化
1. 代码分割
2. 懒加载组件
3. 缓存策略
4. 资源压缩

### 后端优化
1. 数据库索引优化
2. 缓存使用
3. 异步处理
4. 负载均衡

## 安全考虑

### 1. 认证与授权
- JWT Token 验证
- 角色权限控制
- 请求签名验证

### 2. 数据安全
- 使用 HTTPS
- 数据加密存储
- XSS 防护
- CSRF 防护

### 3. 服务安全
- 限流控制
- 防 DDoS 攻击
- 日志审计
- 备份策略