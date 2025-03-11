# API Documentation

## Basic Information
- Base Path: `/api/v1`
- Authentication: Bearer Token
- Response Format: JSON
- Encoding: UTF-8

## Status Codes
| Status Code | Description |
|------------|-------------|
| 200 | Success |
| 400 | Bad Request |
| 401 | Unauthorized or Authentication Failed |
| 403 | Forbidden |
| 404 | Resource Not Found |
| 500 | Internal Server Error |
| 502 | Bad Gateway |
| 503 | Service Unavailable |

## Authentication Endpoints

### Login
```
POST /auth/token
Request:
{
    username: string
    password: string
}
Response:
{
    access_token: string
    token_type: string
}
```

### Register
```
POST /auth/register
Request:
{
    username: string
    email: string
    password: string
}
Response:
{
    id: number
    username: string
    email: string
    role: string
    status: string
}
```

## Chat Endpoints

### Send Message
```
POST /chat
Request:
{
    message: string
    session_id?: number
    system_prompt?: string
    temperature?: number
    max_tokens?: number
}
Response:
{
    session_id: number
    message: {
        id: number
        role: string
        content: string
        created_at: string
        tokens: number
    }
    total_tokens: number
}
```

### List Sessions
```
GET /chat/sessions
Query Parameters:
- skip: number (default: 0)
- limit: number (default: 20)

Response:
Array<{
    id: number
    title: string
    status: string
    message_count: number
    last_message_time: string
    created_at: string
    updated_at: string
}>
```

### Get Session Messages
```
GET /chat/sessions/{session_id}/messages
Query Parameters:
- skip: number (default: 0)
- limit: number (default: 50)

Response:
Array<{
    id: number
    role: string
    content: string
    created_at: string
    tokens: number
    status: string
}>
```

## Statistics Endpoints

### Get Daily Statistics
```
GET /statistics/daily
Query Parameters:
- start_date: string (YYYY-MM-DD)
- end_date: string (YYYY-MM-DD)

Response:
Array<{
    date: string
    chat_count: number
    message_count: number
    avg_response_time: number
    token_usage: number
    error_count: number
}>
```

### Get Total Statistics
```
GET /statistics/total
Response:
{
    total_chats: number
    total_messages: number
    avg_response_time: number
    total_tokens: number
    total_errors: number
}
```

## WebSocket Interface

### Real-time Message Updates
```
WebSocket: /ws/chat/{session_id}

Message Format:
{
    type: "message" | "typing" | "error"
    data: {
        id?: number
        role?: string
        content?: string
        status?: string
        error?: string
    }
}
```

## Rate Limiting
- Authentication endpoints: 5 requests per minute per IP
- Chat endpoints: 60 requests per minute per user
- WebSocket connections: 5 concurrent connections per user

## Error Codes

### HTTP Status Codes
| Status Code | Description | Handling Suggestion |
|-------------|-------------|---------------------|
| 400 | Bad Request | Check if the request parameters are correct |
| 401 | Unauthorized | Check if the authentication information is correct and if the token has expired |
| 403 | Forbidden | Confirm if the user's permission level meets the requirements |
| 404 | Not Found | Check if the resource path is correct |
| 429 | Too Many Requests | Reduce the request frequency and check if it meets the rate limiting rules |
| 500 | Internal Server Error | Check the server logs to locate the specific error |
| 502 | Bad Gateway | Check if the service is running normally and if the network connection is normal |
| 503 | Service Unavailable | Check the server load and confirm if the service needs to be scaled up |

### Business Error Codes
| Error Code | Description | Handling Suggestion |
|------------|-------------|---------------------|
| AUTH001 | Incorrect username or password | Prompt the user to check the input information |
| AUTH002 | Token expired | Guide the user to log in again |
| AUTH003 | Invalid token | Clear the local token cache and log in again |
| CHAT001 | Failed to create session | Check user quota and system resources |
| CHAT002 | Failed to send message | Check the network connection and API status |
| CHAT003 | Failed to retrieve context | Check if the session ID is valid |
| SYS001 | System maintenance | Wait for the system maintenance to complete |
| SYS002 | Insufficient resources | Consider scaling up the system or optimizing resource usage |

Error Response Format:
```json
{
    "error": {
        "code": "string",
        "message": "string",
        "details": "string"
    }
}
```