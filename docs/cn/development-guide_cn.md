# 知答 - 开发规范

## 1. 代码风格规范

### 1.1 TypeScript/JavaScript规范
- 使用 TypeScript 开发
- 使用 ESLint + Prettier 格式化代码
- 遵循以下规则：
  ```javascript
  module.exports = {
    semi: false,          // 不使用分号
    singleQuote: true,    // 使用单引号
    trailingComma: 'none', // 不使用尾逗号
    printWidth: 80,       // 每行最大长度
    tabWidth: 2,         // 缩进空格数
    endOfLine: 'lf'      // 换行符使用 lf
  }
  ```

### 1.2 Vue组件规范
- 使用 Composition API
- 组件文件名使用 PascalCase
- Props 必须指定类型
- 每个组件一个文件
- 组件结构遵循：
  ```vue
  <template>
    <!-- 模板部分 -->
  </template>
  
  <script setup lang="ts">
  // 导入语句
  // 类型定义
  // 响应式数据
  // 计算属性
  // 方法定义
  // 生命周期钩子
  </script>
  
  <style scoped>
  /* 样式定义 */
  </style>
  ```

### 1.3 Python代码规范
- 遵循 PEP 8 规范
- 使用 Black 格式化代码
- 配置示例：
  ```toml
  # pyproject.toml
  [tool.black]
  line-length = 88
  target-version = ['py38']
  include = '\.pyi?$'
  ```
- 类型注解必须
- 文档字符串必须

## 2. 提交规范

### 2.1 Git提交信息
遵循Angular提交规范：
```
<type>(<scope>): <subject>

<body>

<footer>
```

类型(type)：
- feat: 新功能
- fix: 修复bug
- docs: 文档更新
- style: 代码格式化
- refactor: 代码重构
- perf: 性能优化
- test: 测试相关
- chore: 构建/工具链/辅助工具的变动

示例：
```
feat(auth): implement JWT authentication

- Add JWT token generation
- Add token validation middleware
- Update login endpoint to return token

Closes #123
```

### 2.2 分支管理
- 主分支：
  - main: 生产环境分支
  - develop: 开发环境分支
  
- 临时分支：
  - feature/*: 功能分支
  - bugfix/*: 缺陷修复分支
  - hotfix/*: 紧急修复分支
  - release/*: 发布分支

分支命名规范：
```
feature/user-auth     # 功能分支
bugfix/login-error   # 缺陷修复分支
hotfix/api-500      # 紧急修复分支
release/v1.0.0      # 发布分支
```

### 2.3 Pull Request规范
PR标题格式：
```
[类型] 标题描述

例如：
[Feature] Add user authentication
[Fix] Resolve login page issues
[Docs] Update API documentation
```

PR描述模板：
```markdown
## 变更说明
简要说明本次变更的内容

## 相关任务
- 关联的Issue编号
- 需求文档链接

## 测试说明
- 已完成的测试项
- 测试结果
- 测试覆盖率

## 其他说明
- 性能影响
- 向后兼容性
- 其他需要注意的事项
```

## 3. 项目结构规范

### 3.1 前端项目结构
```
frontend/
├── src/
│   ├── assets/        # 静态资源
│   ├── components/    # 公共组件
│   ├── composables/   # 组合式函数
│   ├── layouts/       # 布局组件
│   ├── router/        # 路由配置
│   ├── stores/        # 状态管理
│   ├── styles/        # 全局样式
│   ├── types/         # 类型定义
│   ├── utils/         # 工具函数
│   └── views/         # 页面组件
├── tests/             # 测试文件
├── public/            # 公共资源
└── package.json       # 项目配置
```

### 3.2 后端项目结构
```
backend/
├── src/
│   ├── api/          # API定义
│   │   ├── routers/  # 路由模块
│   │   └── models/   # 数据模型
│   ├── core/         # 核心功能
│   ├── services/     # 业务服务
│   ├── utils/        # 工具函数
│   └── config/       # 配置模块
├── tests/            # 测试文件
├── alembic/          # 数据库迁移
└── requirements.txt  # 项目依赖
```

## 4. 文档规范

### 4.1 代码注释规范
TypeScript/JavaScript注释：
```typescript
/**
 * 函数描述
 * @param {string} param1 - 参数1描述
 * @param {number} param2 - 参数2描述
 * @returns {boolean} 返回值描述
 * @throws {Error} 异常描述
 */
function example(param1: string, param2: number): boolean {
  // 实现细节注释
  return true
}
```

Python注释：
```python
def example(param1: str, param2: int) -> bool:
    """函数描述

    Args:
        param1 (str): 参数1描述
        param2 (int): 参数2描述

    Returns:
        bool: 返回值描述

    Raises:
        ValueError: 异常描述
    """
    # 实现细节注释
    return True
```

### 4.2 接口文档规范
使用OpenAPI(Swagger)规范：
```python
@router.post("/user/login")
async def login(
    credentials: LoginCredentials,
    response: Response,
) -> Token:
    """用户登录接口

    Args:
        credentials: 登录凭证
        response: 响应对象

    Returns:
        Token: 包含access_token的响应

    Raises:
        HTTPException: 登录失败时抛出
    """
```

### 4.3 README文档规范
项目README必须包含：
- 项目简介
- 技术栈说明
- 环境要求
- 安装步骤
- 开发指南
- 部署说明
- 贡献指南
- 许可证信息

## 5. 测试规范

### 5.1 单元测试
- 使用Jest(前端)和pytest(后端)
- 测试文件命名：*.test.ts/*.spec.ts/*.test.py
- 测试覆盖率要求：>80%
- 测试用例规范：
```typescript
describe('模块名称', () => {
  beforeEach(() => {
    // 测试准备
  })

  test('should 预期行为', () => {
    // 测试实现
  })

  afterEach(() => {
    // 测试清理
  })
})
```

### 5.2 端到端测试
- 使用Cypress
- 关键流程必须有E2E测试
- 测试用例组织：
```typescript
describe('功能模块', () => {
  before(() => {
    // 测试准备
  })

  it('should 完成特定操作', () => {
    // 测试步骤
  })
})
```

## 6. CI/CD规范

### 6.1 持续集成
```yaml
# .gitlab-ci.yml
stages:
  - lint
  - test
  - build
  - deploy

lint:
  stage: lint
  script:
    - npm run lint
    - black --check .

test:
  stage: test
  script:
    - npm run test
    - pytest

build:
  stage: build
  script:
    - npm run build
    - docker build .
```

### 6.2 部署流程
1. 开发环境
   - 代码推送触发
   - 自动化测试
   - 自动部署

2. 测试环境
   - 手动触发
   - 完整测试
   - 自动部署

3. 生产环境
   - 手动审批
   - 灰度发布
   - 回滚机制

## 7. 安全规范

### 7.1 代码安全
- 禁止硬编码敏感信息
- 使用环境变量配置
- 日志脱敏处理
- 定期代码扫描

### 7.2 认证授权
- 统一认证中心
- 基于角色的权限控制
- 操作审计日志
- 会话安全管理

### 7.3 数据安全
- 敏感数据加密
- 传输加密(HTTPS)
- 定期备份策略
- 访问控制机制