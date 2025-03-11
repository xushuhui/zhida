# 知答 - 数据库设计文档

## 1. 数据库选型
使用MySQL作为主数据库，Redis作为缓存数据库。选择理由：
- MySQL提供强大的事务支持和数据一致性保证
- MySQL具有成熟的生态系统和优秀的性能
- Redis提供高性能的缓存和实时数据支持
- 两者都支持分布式部署

## 2. 表设计

### 2.1 users - 用户表
```sql
CREATE TABLE users (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    avatar VARCHAR(255),
    role ENUM('admin', 'user') NOT NULL DEFAULT 'user',
    status ENUM('active', 'disabled') NOT NULL DEFAULT 'active',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL,
    preferences JSON
);

-- 索引
CREATE INDEX idx_users_created_at ON users(created_at DESC);
```

### 2.2 sessions - 会话表
```sql
CREATE TABLE sessions (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT UNSIGNED NOT NULL,
    title VARCHAR(255) NOT NULL,
    status ENUM('active', 'archived') NOT NULL DEFAULT 'active',
    message_count INT UNSIGNED DEFAULT 0,
    last_message_time TIMESTAMP NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    system_prompt TEXT,
    temperature DECIMAL(3,2),
    max_tokens INT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 索引
CREATE INDEX idx_sessions_user_id ON sessions(user_id);
CREATE INDEX idx_sessions_created_at ON sessions(created_at DESC);
CREATE INDEX idx_sessions_last_message ON sessions(last_message_time DESC);
```

### 2.3 messages - 消息表
```sql
CREATE TABLE messages (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    session_id BIGINT UNSIGNED NOT NULL,
    user_id BIGINT UNSIGNED NOT NULL,
    role ENUM('user', 'assistant', 'system') NOT NULL,
    content TEXT NOT NULL,
    tokens INT UNSIGNED,
    status ENUM('sent', 'delivered', 'error') NOT NULL DEFAULT 'sent',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    response_time INT UNSIGNED,
    client_info VARCHAR(255),
    ip_address VARCHAR(45),
    FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 索引
CREATE INDEX idx_messages_session ON messages(session_id);
CREATE INDEX idx_messages_user ON messages(user_id);
CREATE INDEX idx_messages_created ON messages(created_at DESC);
CREATE INDEX idx_messages_role ON messages(role);
```

### 2.4 statistics - 统计表
```sql
CREATE TABLE statistics (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT UNSIGNED NOT NULL,
    date DATE NOT NULL,
    chat_count INT UNSIGNED DEFAULT 0,
    message_count INT UNSIGNED DEFAULT 0,
    avg_response_time FLOAT,
    token_usage BIGINT UNSIGNED DEFAULT 0,
    error_count INT UNSIGNED DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_date (user_id, date)
);

-- 索引
CREATE INDEX idx_statistics_date ON statistics(date DESC);
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

### 4.1 MySQL备份
- 每日全量备份 (mysqldump)
- 开启二进制日志实现实时备份
- 定期数据一致性检查
- 备份文件加密存储

### 4.2 Redis备份
- RDB快照: 每小时
- AOF日志: 实时
- 主从复制配置

## 5. 扩展性设计

### 5.1 分区策略
- 按用户ID范围分区
- 按时间范围分区
- 热数据优先处理

### 5.2 索引优化
- 复合索引设计
- 执行计划分析
- 定期索引维护和统计信息更新

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