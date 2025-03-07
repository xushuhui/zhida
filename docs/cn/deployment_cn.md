# 部署文档

## 1. 环境需求

### 1.1 硬件要求
- CPU: 2核心或以上
- 内存: 4GB或以上
- 存储: 20GB或以上
- 网络带宽: 5Mbps或以上

### 1.2 软件要求
- 操作系统: Ubuntu 20.04 LTS 或更高版本
- Docker: 20.10 或更高版本
- Docker Compose: 2.0 或更高版本
- Nginx: 1.18 或更高版本

### 1.3 第三方服务
- OpenAI API 密钥
- Redis (可选，用于缓存)
- MongoDB (可选，用于数据持久化)

## 2. Docker部署

### 2.1 目录结构
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

### 2.2 Docker配置

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
    volumes:
      - ../backend:/app

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
```

#### frontend/Dockerfile
```dockerfile
# 构建阶段
FROM node:16-alpine as build-stage
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# 生产阶段
FROM nginx:stable-alpine as production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

#### backend/Dockerfile
```dockerfile
FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "run.py"]
```

### 2.3 Nginx配置

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

## 3. 服务器部署步骤

### 3.1 基础环境配置
```bash
# 更新系统
apt-get update && apt-get upgrade -y

# 安装必要工具
apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# 安装Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# 安装Docker Compose
curl -L "https://github.com/docker/compose/releases/download/v2.5.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
```

### 3.2 项目部署
```bash
# 克隆项目
git clone <repository_url>
cd <project_directory>

# 创建环境变量文件
cp .env.example .env
# 编辑.env文件，填入必要的环境变量

# 启动服务
docker-compose up -d

# 查看服务状态
docker-compose ps
```

### 3.3 SSL证书配置（使用Let's Encrypt）
```bash
# 安装certbot
apt-get install -y certbot python3-certbot-nginx

# 获取证书
certbot --nginx -d example.com -d www.example.com

# 自动续期证书
certbot renew --dry-run
```

## 4. 监控与维护

### 4.1 日志管理
```bash
# 查看容器日志
docker-compose logs -f [service_name]

# 配置日志轮转
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

### 4.2 健康检查
```bash
# 创建健康检查脚本
cat > healthcheck.sh << EOF
#!/bin/bash

# 检查前端服务
curl -f http://localhost:80 || exit 1

# 检查后端服务
curl -f http://localhost:8000/health || exit 1

# 检查数据库连接
docker-compose exec backend python -c "from db import db; db.ping()" || exit 1
EOF

chmod +x healthcheck.sh
```

### 4.3 备份策略
```bash
# 创建备份脚本
cat > backup.sh << EOF
#!/bin/bash

# 备份数据库
docker-compose exec -T mongodb mongodump --out /backup/\$(date +%Y%m%d)

# 备份环境配置
cp .env /backup/env/\$(date +%Y%m%d)

# 压缩备份
tar -czf /backup/backup_\$(date +%Y%m%d).tar.gz /backup/\$(date +%Y%m%d)

# 删除30天前的备份
find /backup -type f -name "*.tar.gz" -mtime +30 -delete
EOF

chmod +x backup.sh

# 添加到crontab
echo "0 2 * * * /path/to/backup.sh" >> /etc/crontab
```

## 5. 扩展与优化

### 5.1 负载均衡配置
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

### 5.2 缓存配置
```nginx
# Nginx缓存配置
proxy_cache_path /tmp/nginx_cache levels=1:2 keys_zone=my_cache:10m max_size=10g inactive=60m use_temp_path=off;

location / {
    proxy_cache my_cache;
    proxy_cache_use_stale error timeout http_500 http_502 http_503 http_504;
    proxy_cache_valid 200 60m;
}
```

### 5.3 性能优化
```nginx
# Nginx性能优化
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
    
    # 开启gzip压缩
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
}
```