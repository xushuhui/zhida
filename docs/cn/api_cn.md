# API 文档

## 基础信息
- 基础路径：`/api/v1`
- 认证方式：Bearer Token
- 响应格式：JSON
- 编码方式：UTF-8

## 错误码说明
| 状态码 | 说明 |
|-------|------|
| 200 | 请求成功 |
| 400 | 请求参数错误 |
| 401 | 未认证或认证失败 |
| 403 | 权限不足 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

## 认证接口

### 用户登录
- 请求路径：`POST /login`
- 请求参数：
  ```typescript
  {
    username: string  // 用户名
    password: string  // 密码
  }
  ```
- 响应数据：
  ```typescript
  {
    access_token: string  // JWT令牌
    token_type: string    // 令牌类型，固定为"bearer"
  }
  ```
- 错误响应：
  ```typescript
  {
    detail: string  // 错误详情
  }
  ```

### 用户登出
- 请求路径：`POST /logout`
- 请求头：需要包含有效的Authorization Token
- 响应数据：
  ```typescript
  {
    message: string  // "成功登出"
  }
  ```

## 对话接口

### 发送消息
- 请求路径：`POST /chat`
- 请求头：需要包含有效的Authorization Token
- 请求参数：
  ```typescript
  {
    message: string  // 用户发送的消息内容
  }
  ```
- 响应数据：
  ```typescript
  {
    response: string       // AI助手的回复内容
    messages: Array<{     // 当前会话的所有消息记录
      role: string        // 消息角色：'user' 或 'assistant'
      content: string     // 消息内容
      timestamp: string   // 消息时间戳，ISO 8601格式
    }>
  }
  ```

### 获取历史记录
- 请求路径：`GET /chat/history`
- 请求头：需要包含有效的Authorization Token
- 查询参数：
  ```typescript
  {
    page?: number      // 可选，页码，默认为1
    pageSize?: number  // 可选，每页条数，默认为20
  }
  ```
- 响应数据：
  ```typescript
  {
    messages: Array<{
      role: string      // 消息角色：'user' 或 'assistant'
      content: string   // 消息内容
      timestamp: string // 消息时间戳，ISO 8601格式
    }>,
    pagination: {
      total: number     // 总记录数
      page: number      // 当前页码
      pageSize: number  // 每页条数
    }
  }
  ```

## 统计接口

### 获取对话统计
- 请求路径：`GET /stats/chat`
- 请求头：需要包含有效的Authorization Token
- 响应数据：
  ```typescript
  {
    todayChats: number        // 今日对话数
    totalChats: number        // 总对话数
    avgResponseTime: number   // 平均响应时间(ms)
    satisfactionRate: number  // 满意度(百分比)
  }
  ```

### 获取消息统计
- 请求路径：`GET /stats/messages`
- 请求头：需要包含有效的Authorization Token
- 响应数据：
  ```typescript
  {
    todayMessages: number     // 今日消息数
    totalMessages: number     // 总消息数
    avgMessagesPerChat: number// 平均每个对话的消息数
  }
  ```

## WebSocket 接口

### 实时消息推送
- 连接地址：`ws://[host]/ws/chat`
- 认证方式：通过URL参数传递token
  ```
  ws://[host]/ws/chat?token=[access_token]
  ```
- 消息格式：
  ```typescript
  // 发送消息
  {
    type: 'message'
    content: string
  }

  // 接收消息
  {
    type: 'message' | 'status'
    data: {
      role: string
      content: string
      timestamp: string
    }
  }
  ```

## 数据模型

### Message
```typescript
interface Message {
  id: string           // 消息ID
  role: string         // 角色：'user' 或 'assistant'
  content: string      // 消息内容
  timestamp: string    // 时间戳
  sessionId: string    // 会话ID
  status: string       // 消息状态：'sent', 'delivered', 'read'
}
```

### Chat Session
```typescript
interface ChatSession {
  id: string           // 会话ID
  userId: string       // 用户ID
  startTime: string    // 开始时间
  lastMessageTime: string // 最后消息时间
  messageCount: number // 消息数量
}
```

## 限流说明
- 登录接口：每IP每分钟最多5次请求
- 对话接口：每用户每分钟最多60次请求
- WebSocket连接：每用户最多同时3个连接

# API Documentation
## Basic Information
- Base Path: `/api/v1`
- Authentication: Bearer Token
- Response Format: JSON
- Encoding: UTF-8

## Status Codes
| Status Code | Description |
|------------|-------------|
| 200 | Request Successful |
| 400 | Bad Request |
| 401 | Unauthorized or Authentication Failed |
| 403 | Forbidden |
| 404 | Resource Not Found |
| 500 | Internal Server Error |

## Authentication Endpoints
### User Login
- Path: `POST /login`
- Request Body:
  ```typescript
  {
    username: string  // Username
    password: string  // Password
  }
  ```
- Response:
  ```typescript
  {
    access_token: string  // JWT Token
    token_type: string    // Token type, always "bearer"
  }
  ```
- Error Response:
  ```typescript
  {
    detail: string  // Error details
  }
  ```

### User Logout
- Path: `POST /logout`
- Headers: Requires valid Authorization Token
- Response:
  ```typescript
  {
    message: string  // "Successfully logged out"
  }
  ```

## Chat Endpoints
### Send Message
- Path: `POST /chat`
- Headers: Requires valid Authorization Token
- Request Body:
  ```typescript
  {
    message: string  // User message content
  }
  ```
- Response:
  ```typescript
  {
    response: string       // AI assistant's response
    messages: Array<{     // All messages in current session
      role: string        // Message role: 'user' or 'assistant'
      content: string     // Message content
      timestamp: string   // Timestamp in ISO 8601 format
    }>
  }
  ```

### Get Chat History
- Path: `GET /chat/history`
- Headers: Requires valid Authorization Token
- Query Parameters:
  ```typescript
  {
    page?: number      // Optional, page number, defaults to 1
    pageSize?: number  // Optional, items per page, defaults to 20
  }
  ```
- Response:
  ```typescript
  {
    messages: Array<{
      role: string      // Message role: 'user' or 'assistant'
      content: string   // Message content
      timestamp: string // Timestamp in ISO 8601 format
    }>,
    pagination: {
      total: number     // Total records
      page: number      // Current page
      pageSize: number  // Items per page
    }
  }
  ```

## Statistics Endpoints
### Get Chat Statistics
- Path: `GET /stats/chat`
- Headers: Requires valid Authorization Token
- Response:
  ```typescript
  {
    todayChats: number        // Chats today
    totalChats: number        // Total chats
    avgResponseTime: number   // Average response time (ms)
    satisfactionRate: number  // Satisfaction rate (percentage)
  }
  ```

### Get Message Statistics
- Path: `GET /stats/messages`
- Headers: Requires valid Authorization Token
- Response:
  ```typescript
  {
    todayMessages: number      // Messages today
    totalMessages: number      // Total messages
    avgMessagesPerChat: number // Average messages per chat
  }
  ```

## WebSocket Interface
### Real-time Message Push
- Connection URL: `ws://[host]/ws/chat`
- Authentication: Pass token as URL parameter
  ```
  ws://[host]/ws/chat?token=[access_token]
  ```
- Message Format:
  ```typescript
  // Send message
  {
    type: 'message'
    content: string
  }
  // Receive message
  {
    type: 'message' | 'status'
    data: {
      role: string
      content: string
      timestamp: string
    }
  }
  ```

## Data Models
### Message
```typescript
interface Message {
  id: string           // Message ID
  role: string         // Role: 'user' or 'assistant'
  content: string      // Message content
  timestamp: string    // Timestamp
  sessionId: string    // Session ID
  status: string       // Message status: 'sent', 'delivered', 'read'
}
```

### Chat Session
```typescript
interface ChatSession {
  id: string           // Session ID
  userId: string       // User ID
  startTime: string    // Start time
  lastMessageTime: string // Last message time
  messageCount: number // Message count
}
```

## Rate Limiting
- Login endpoint: 5 requests per minute per IP
- Chat endpoint: 60 requests per minute per user
- WebSocket connection: Maximum 3 concurrent connections per user