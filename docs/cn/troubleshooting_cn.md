# 知答 - 常见问题解决方案

## 1. 部署问题

### 1.1 环境配置问题
#### 问题：Node.js版本兼容性错误
**症状**：启动前端项目时报错 "Error: Node.js v16.0.0 or higher is required"
**解决方案**：
1. 检查Node.js版本：`node -v`
2. 如果版本过低，下载并安装最新LTS版本
3. 使用nvm管理多个Node.js版本：
```bash
nvm install 16
nvm use 16
```

#### 问题：Python依赖安装失败
**症状**：运行 `pip install -r requirements.txt` 时出错
**解决方案**：
1. 更新pip：`python -m pip install --upgrade pip`
2. 使用虚拟环境：
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows
```
3. 单独安装问题依赖，查看具体错误信息

### 1.2 Docker部署问题
#### 问题：容器启动失败
**症状**：docker-compose up 后服务无法访问
**解决方案**：
1. 检查日志：`docker-compose logs`
2. 确认端口映射：`docker ps`
3. 检查网络配置：`docker network ls`
4. 常见修复步骤：
```bash
# 重建容器
docker-compose down
docker-compose up --build

# 检查端口占用
netstat -an | grep 3000
netstat -an | grep 8000
```

## 2. 运行时问题

### 2.1 前端问题
#### 问题：登录认证失败
**症状**：登录后立即被退出或无法访问受保护路由
**解决方案**：
1. 检查localStorage中的token：
```javascript
// 浏览器控制台
localStorage.getItem('access_token')
```
2. 检查token格式和有效期
3. 确认API请求头中包含token：
```javascript
// 请求拦截器配置
axios.interceptors.request.use(config => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})
```

#### 问题：WebSocket连接异常
**症状**：实时消息推送失败，连接频繁断开
**解决方案**：
1. 实现重连机制：
```javascript
let reconnectAttempts = 0
const maxReconnectAttempts = 5

function connectWebSocket() {
  const ws = new WebSocket(WS_URL)
  
  ws.onclose = () => {
    if (reconnectAttempts < maxReconnectAttempts) {
      setTimeout(() => {
        reconnectAttempts++
        connectWebSocket()
      }, 1000 * Math.pow(2, reconnectAttempts))
    }
  }
  
  ws.onopen = () => {
    reconnectAttempts = 0
  }
}
```

2. 添加心跳检测：
```javascript
setInterval(() => {
  if (ws.readyState === WebSocket.OPEN) {
    ws.send('ping')
  }
}, 30000)
```

### 2.2 后端问题
#### 问题：OpenAI API调用失败
**症状**：发送消息后返回500错误
**解决方案**：
1. 检查API密钥配置
2. 验证API配额和计费状态
3. 实现错误重试机制：
```python
import time
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
async def call_openai_api(messages):
    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=messages
        )
        return response
    except Exception as e:
        logger.error(f"OpenAI API error: {str(e)}")
        raise
```

#### 问题：数据库连接断开
**症状**：随机出现数据库操作错误
**解决方案**：
1. 实现连接池：
```python
from motor.motor_asyncio import AsyncIOMotorClient

class Database:
    client: AsyncIOMotorClient = None

    @classmethod
    async def connect_db(cls):
        cls.client = AsyncIOMotorClient(
            settings.MONGODB_URL,
            maxPoolSize=10,
            minPoolSize=5,
            serverSelectionTimeoutMS=5000
        )
        try:
            await cls.client.admin.command('ping')
            logger.info("Connected to MongoDB")
        except Exception as e:
            logger.error(f"MongoDB connection error: {str(e)}")
            raise

    @classmethod
    async def close_db(cls):
        if cls.client:
            await cls.client.close()
```

2. 添加健康检查：
```python
async def db_health_check():
    try:
        await Database.client.admin.command('ping')
        return True
    except Exception:
        return False
```

## 3. 性能问题

### 3.1 前端性能优化
#### 问题：页面加载缓慢
**解决方案**：
1. 路由懒加载：
```javascript
const routes = [
  {
    path: '/chat',
    component: () => import('@/views/ChatView.vue')
  }
]
```

2. 组件按需导入：
```javascript
import { defineAsyncComponent } from 'vue'

const AsyncComponent = defineAsyncComponent(() =>
  import('./components/HeavyComponent.vue')
)
```

3. 资源预加载：
```javascript
const imageLoader = new Image()
imageLoader.src = '/large-image.jpg'
```

### 3.2 后端性能优化
#### 问题：API响应速度慢
**解决方案**：
1. 使用缓存：
```python
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

@router.get("/chat/history")
@cache(expire=300)  # 缓存5分钟
async def get_chat_history():
    # ...
```

2. 异步处理：
```python
from fastapi import BackgroundTasks

@router.post("/chat")
async def create_chat(
    message: str,
    background_tasks: BackgroundTasks
):
    # 立即返回响应
    response = {"status": "processing"}
    # 后台处理耗时任务
    background_tasks.add_task(process_message, message)
    return response
```

## 4. 安全问题

### 4.1 XSS防护
#### 问题：消息内容可能包含恶意脚本
**解决方案**：
1. 使用DOMPurify清理内容：
```javascript
import DOMPurify from 'dompurify'

const sanitizedMessage = DOMPurify.sanitize(message)
```

2. 配置CSP头：
```nginx
add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline';"
```

### 4.2 CSRF防护
#### 问题：可能受到CSRF攻击
**解决方案**：
1. 配置CSRF Token：
```python
from fastapi import Depends, Cookie, HTTPException
from fastapi.security import HTTPBearer

security = HTTPBearer()

async def verify_csrf_token(
    csrf_token: str = Cookie(None),
    authorization: str = Depends(security)
):
    if not csrf_token or csrf_token != generate_csrf_token(authorization):
        raise HTTPException(status_code=403, detail="Invalid CSRF token")
```

2. 前端请求时携带token：
```javascript
axios.defaults.headers.common['X-CSRF-TOKEN'] = getCsrfToken()
```

## 5. 监控告警

### 5.1 系统监控
#### 问题：缺乏系统监控能力
**解决方案**：
1. 使用Prometheus + Grafana：
```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'zhida'
    static_configs:
      - targets: ['localhost:8000']
```

2. 应用埋点：
```python
from prometheus_client import Counter, Histogram

request_count = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint']
)

response_time = Histogram(
    'http_response_time_seconds',
    'HTTP response time in seconds',
    ['method', 'endpoint']
)
```

### 5.2 错误追踪
#### 问题：错误难以复现和定位
**解决方案**：
1. 使用Sentry进行错误追踪：
```python
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastAPIIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[FastAPIIntegration()]
)
```

2. 自定义错误上报：
```python
try:
    # 可能出错的代码
    raise Exception("Something went wrong")
except Exception as e:
    sentry_sdk.capture_exception(e)
```