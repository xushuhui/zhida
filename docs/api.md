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