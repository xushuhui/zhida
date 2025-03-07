# ZhiDa - Database Design Documentation
## 1. Database Selection
MongoDB is used as the primary database and Redis as the cache database. Reasons for selection:
- MongoDB is suitable for storing unstructured conversation data
- Redis provides high-performance caching and real-time data support
- Both support distributed deployment

## 2. Collection (Table) Design
### 2.1 users - User Collection
```javascript
{
  _id: ObjectId,              // User ID
  username: String,           // Username
  password: String,           // Encrypted password
  email: String,             // Email
  avatar: String,            // Avatar URL
  role: String,              // Role: admin/user
  status: String,            // Status: active/disabled
  created_at: DateTime,      // Creation time
  updated_at: DateTime,      // Update time
  last_login: DateTime,      // Last login time
  preferences: {             // User preferences
    language: String,        // Interface language
    theme: String,          // Theme setting
    notification: Boolean   // Notification switch
  }
}
// Indexes
{
  username: 1,        // Unique username index
  email: 1,          // Unique email index
  created_at: -1     // Creation time descending index
}
```

### 2.2 sessions - Session Collection
```javascript
{
  _id: ObjectId,              // Session ID
  user_id: ObjectId,         // User ID
  title: String,             // Session title
  status: String,            // Status: active/archived
  message_count: Number,     // Message count
  last_message_time: DateTime, // Last message time
  created_at: DateTime,      // Creation time
  updated_at: DateTime,      // Update time
  context: {                 // Session context
    system_prompt: String,   // System prompt
    temperature: Number,     // GPT parameter
    max_tokens: Number      // Maximum token count
  }
}
// Indexes
{
  user_id: 1,              // User ID index
  created_at: -1,          // Creation time descending index
  last_message_time: -1   // Last message time descending index
}
```

### 2.3 messages - Message Collection
```javascript
{
  _id: ObjectId,              // Message ID
  session_id: ObjectId,      // Session ID
  user_id: ObjectId,         // User ID
  role: String,              // Role: user/assistant/system
  content: String,           // Message content
  tokens: Number,            // Token count
  status: String,            // Status: sent/delivered/error
  created_at: DateTime,      // Creation time
  response_time: Number,     // Response time (ms)
  metadata: {                // Metadata
    client_info: String,     // Client information
    ip_address: String      // IP address
  }
}
// Indexes
{
  session_id: 1,           // Session ID index
  user_id: 1,             // User ID index
  created_at: -1,         // Creation time descending index
  role: 1                 // Role index
}
```

### 2.4 statistics - Statistics Collection
```javascript
{
  _id: ObjectId,              // Statistics ID
  user_id: ObjectId,         // User ID
  date: Date,                // Statistics date
  chat_count: Number,        // Chat count
  message_count: Number,     // Message count
  avg_response_time: Number, // Average response time
  token_usage: Number,       // Token usage
  error_count: Number,       // Error count
  created_at: DateTime       // Creation time
}
// Indexes
{
  user_id: 1,              // User ID index
  date: -1                // Date descending index
}
```

## 3. Redis Cache Design
### 3.1 User Token Cache
```
Key: user:token:{user_id}
Value: JWT Token
Expiry: 30 minutes
```

### 3.2 User Session List Cache
```
Key: user:sessions:{user_id}
Value: List of session objects
Expiry: 1 hour
```

### 3.3 Session Message Cache
```
Key: session:messages:{session_id}
Value: List of latest 50 messages
Expiry: 2 hours
```

### 3.4 Statistics Data Cache
```
Key: stats:daily:{date}
Value: Hash of statistics
Expiry: 24 hours
```

### 3.5 Rate Limiting
```
Key: ratelimit:user:{user_id}
Value: Counter
Expiry: 1 minute
```

## 4. Backup Strategy
### 4.1 MongoDB Backup
- Daily full backup
- Real-time operation log backup
- Regular data consistency check
- Encrypted backup storage

### 4.2 Redis Backup
- RDB snapshot: Hourly
- AOF log: Real-time
- Master-slave replication configuration

## 5. Scalability Design
### 5.1 Sharding Strategy
- Sharding by user ID
- Session data localization
- Hot data priority migration

### 5.2 Index Optimization
- Compound index design
- Index coverage queries
- Regular index rebuilding

## 6. Data Security
### 6.1 Access Control
- Role-based access control
- Field-level permission control
- Operation audit logs

### 6.2 Data Encryption
- Sensitive information encryption
- Data transmission encryption
- Backup data encryption

## 7. Performance Optimization
### 7.1 Query Optimization
- Index coverage queries
- Batch operation optimization
- Aggregation pipeline optimization

### 7.2 Cache Strategy
- Multi-level cache architecture
- Cache warming mechanism
- Cache update strategy