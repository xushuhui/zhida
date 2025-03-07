# 知答 - 数据库设计文档

## 1. 数据库选型
使用MongoDB作为主数据库,Redis作为缓存数据库。选择理由:
- MongoDB适合存储非结构化的对话数据
- Redis提供高性能的缓存和实时数据支持
- 两者都支持分布式部署

## 2. 集合(表)设计

### 2.1 users - 用户集合
```javascript
{
  _id: ObjectId,              // 用户ID
  username: String,           // 用户名
  password: String,           // 加密密码
  email: String,             // 邮箱
  avatar: String,            // 头像URL
  role: String,              // 角色: admin/user
  status: String,            // 状态: active/disabled
  created_at: DateTime,      // 创建时间
  updated_at: DateTime,      // 更新时间
  last_login: DateTime,      // 最后登录时间
  preferences: {             // 用户偏好设置
    language: String,        // 界面语言
    theme: String,          // 主题设置
    notification: Boolean   // 通知开关
  }
}

// 索引
{
  username: 1,        // 用户名唯一索引
  email: 1,          // 邮箱唯一索引
  created_at: -1     // 创建时间降序索引
}
```

### 2.2 sessions - 会话集合
```javascript
{
  _id: ObjectId,              // 会话ID
  user_id: ObjectId,         // 用户ID
  title: String,             // 会话标题
  status: String,            // 状态: active/archived
  message_count: Number,     // 消息数量
  last_message_time: DateTime, // 最后消息时间
  created_at: DateTime,      // 创建时间
  updated_at: DateTime,      // 更新时间
  context: {                 // 会话上下文
    system_prompt: String,   // 系统提示语
    temperature: Number,     // GPT参数
    max_tokens: Number      // 最大token数
  }
}

// 索引
{
  user_id: 1,              // 用户ID索引
  created_at: -1,          // 创建时间降序索引
  last_message_time: -1   // 最后消息时间降序索引
}
```

### 2.3 messages - 消息集合
```javascript
{
  _id: ObjectId,              // 消息ID
  session_id: ObjectId,      // 会话ID
  user_id: ObjectId,         // 用户ID
  role: String,              // 角色: user/assistant/system
  content: String,           // 消息内容
  tokens: Number,            // token数量
  status: String,            // 状态: sent/delivered/error
  created_at: DateTime,      // 创建时间
  response_time: Number,     // 响应时间(ms)
  metadata: {                // 元数据
    client_info: String,     // 客户端信息
    ip_address: String      // IP地址
  }
}

// 索引
{
  session_id: 1,           // 会话ID索引
  user_id: 1,             // 用户ID索引
  created_at: -1,         // 创建时间降序索引
  role: 1                 // 角色索引
}
```

### 2.4 statistics - 统计集合
```javascript
{
  _id: ObjectId,              // 统计ID
  user_id: ObjectId,         // 用户ID
  date: Date,                // 统计日期
  chat_count: Number,        // 对话数量
  message_count: Number,     // 消息数量
  avg_response_time: Number, // 平均响应时间
  token_usage: Number,       // token使用量
  error_count: Number,       // 错误次数
  created_at: DateTime       // 创建时间
}

// 索引
{
  user_id: 1,              // 用户ID索引
  date: -1                // 日期降序索引
}
```

## 3. Redis 缓存设计

### 3.1 用户Token缓存
```
Key: user:token:{user_id}
Value: JWT Token
Expiry: 30分钟
```

### 3.2 用户会话列表缓存
```
Key: user:sessions:{user_id}
Value: List of session objects
Expiry: 1小时
```

### 3.3 会话消息缓存
```
Key: session:messages:{session_id}
Value: List of latest 50 messages
Expiry: 2小时
```

### 3.4 统计数据缓存
```
Key: stats:daily:{date}
Value: Hash of statistics
Expiry: 24小时
```

### 3.5 限流控制
```
Key: ratelimit:user:{user_id}
Value: Counter
Expiry: 1分钟
```

## 4. 数据备份策略

### 4.1 MongoDB备份
- 每日全量备份
- 实时操作日志备份
- 定期数据一致性检查
- 备份文件加密存储

### 4.2 Redis备份
- RDB快照: 每小时
- AOF日志: 实时
- 主从复制配置

## 5. 扩展性设计

### 5.1 分片策略
- 按用户ID分片
- 会话数据本地化
- 热数据优先迁移

### 5.2 索引优化
- 复合索引设计
- 索引覆盖查询
- 定期索引重建

## 6. 数据安全

### 6.1 访问控制
- 基于角色的访问控制
- 字段级权限控制
- 操作审计日志

### 6.2 数据加密
- 敏感信息加密
- 传输数据加密
- 备份数据加密

## 7. 性能优化

### 7.1 查询优化
- 索引覆盖查询
- 批量操作优化
- 聚合管道优化

### 7.2 缓存策略
- 多级缓存架构
- 缓存预热机制
- 缓存更新策略