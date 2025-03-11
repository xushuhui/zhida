# 知答 - Deployment Guide

## 1. Environment Requirements

### 1.1 Hardware Requirements
- CPU: 2 cores or more
- Memory: 4GB or more
- Storage: 20GB or more
- Network Bandwidth: 5Mbps or more

### 1.2 Software Requirements
- Operating System: Ubuntu 20.04 LTS or higher
- Docker: 20.10 or higher
- Docker Compose: 2.0 or higher
- Nginx: 1.18 or higher

### 1.3 Third-party Services
- OpenAI API Key
- Redis (optional, for caching)
- MySQL (for data persistence)

## 2. Docker Deployment

### 2.1 Directory Structure
```
deployment/
├── docker-compose.yml
├── nginx/
│   ├── nginx.conf
│   └── conf.d/
│       └── default.conf
├── backend/
│   └── Dockerfile
└── frontend/
    └── Dockerfile
```

### 2.2 Docker Configuration

#### docker-compose.yml
```yaml
version: '3.8'

services:
  frontend:
    build: 
      context: ../frontend
      dockerfile: Dockerfile
    ports:
      - "3000:80"
    depends_on:
      - backend
    environment:
      - VITE_API_URL=http://backend:8000

  backend:
    build:
      context: ../backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - JWT_SECRET_KEY=${JWT_SECRET_KEY}
      - DB_HOST=mysql
      - DB_PORT=3306
      - DB_USER=zhida_user
      - DB_PASSWORD=password
      - DB_NAME=zhida_db
      - REDIS_HOST=redis
    depends_on:
      mysql:
        condition: service_healthy
      redis:
        condition: service_healthy
    volumes:
      - ../backend:/app

  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD:-rootpassword}
      MYSQL_DATABASE: ${MYSQL_DATABASE:-zhida_db}
      MYSQL_USER: ${MYSQL_USER:-zhida_user}
      MYSQL_PASSWORD: ${MYSQL_PASSWORD:-password}
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:6.2-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    command: redis-server --appendonly yes

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./nginx/conf.d:/etc/nginx/conf.d
      - ./certbot/conf:/etc/letsencrypt
      - ./certbot/www:/var/www/certbot
    depends_on:
      - frontend
      - backend

volumes:
  mysql_data:
  redis_data:
```

### 2.3 Nginx Configuration

#### nginx/nginx.conf
```nginx
user  nginx;
worker_processes  auto;

error_log  /var/log/nginx/error.log notice;
pid        /var/run/nginx.pid;

events {
    worker_connections  1024;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;

    sendfile        on;
    keepalive_timeout  65;

    include /etc/nginx/conf.d/*.conf;
}
```

#### nginx/conf.d/default.conf
```nginx
server {
    listen 80;
    server_name localhost;

    location / {
        root   /usr/share/nginx/html;
        index  index.html;
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://backend:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    location /ws {
        proxy_pass http://backend:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "Upgrade";
        proxy_set_header Host $host;
    }
}
```

## 3. Server Deployment Steps

### 3.1 Basic Environment Setup
```bash
# Update system
apt-get update && apt-get upgrade -y

# Install necessary tools
apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Docker Compose
curl -L "https://github.com/docker/compose/releases/download/v2.5.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
```

### 3.2 Project Deployment
```bash
# Clone project
git clone <repository_url>
cd <project_directory>

# Create environment variables file
cp .env.example .env
# Edit .env file with necessary environment variables

# Start services
docker-compose up -d

# Check service status
docker-compose ps
```

### 3.3 SSL Certificate Configuration (Using Let's Encrypt)
```bash
# Install certbot
apt-get install -y certbot python3-certbot-nginx

# Get certificate
certbot --nginx -d example.com -d www.example.com

# Auto-renew certificate
certbot renew --dry-run
```

## 4. Monitoring and Maintenance

### 4.1 Log Management
```bash
# View container logs
docker-compose logs -f [service_name]

# Configure log rotation
cat > /etc/logrotate.d/docker-compose << EOF
/var/lib/docker/containers/*/*.log {
    rotate 7
    daily
    compress
    missingok
    delaycompress
    copytruncate
}
EOF
```

### 4.2 Health Check
```bash
# Create health check script
cat > healthcheck.sh << EOF
#!/bin/bash

# Check frontend service
curl -f http://localhost:80 || exit 1

# Check backend service
curl -f http://localhost:8000/health || exit 1

# Check database connection
docker-compose exec backend python -c "from db import db; db.ping()" || exit 1
EOF

chmod +x healthcheck.sh
```

### 4.3 Backup Strategy
```bash
# Create backup script
cat > backup.sh << EOF
#!/bin/bash

# Backup MySQL database
docker-compose exec -T mysql mysqldump -u root -p\${MYSQL_ROOT_PASSWORD} zhida_db > /backup/\$(date +%Y%m%d).sql

# Backup environment config
cp .env /backup/env/\$(date +%Y%m%d)

# Compress backup
tar -czf /backup/backup_\$(date +%Y%m%d).tar.gz /backup/\$(date +%Y%m%d).sql /backup/env/\$(date +%Y%m%d)

# Delete backups older than 30 days
find /backup -type f -name "*.tar.gz" -mtime +30 -delete
EOF

chmod +x backup.sh

# Add to crontab
echo "0 2 * * * /path/to/backup.sh" >> /etc/crontab
```

## 5. Scaling and Optimization

### 5.1 Load Balancing Configuration
```nginx
upstream backend {
    server backend1:8000;
    server backend2:8000;
    server backend3:8000;
}

upstream frontend {
    server frontend1:80;
    server frontend2:80;
}
```

### 5.2 Cache Configuration
```nginx
# Nginx cache configuration
proxy_cache_path /tmp/nginx_cache levels=1:2 keys_zone=my_cache:10m max_size=10g inactive=60m use_temp_path=off;

location / {
    proxy_cache my_cache;
    proxy_cache_use_stale error timeout http_500 http_502 http_503 http_504;
    proxy_cache_valid 200 60m;
}
```

### 5.3 Performance Optimization
```nginx
# Nginx performance optimization
worker_processes auto;
worker_rlimit_nofile 65535;

events {
    worker_connections 65535;
    multi_accept on;
    use epoll;
}

http {
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;
    server_tokens off;
    
    # Enable gzip compression
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
}
````