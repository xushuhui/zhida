# 知答 Developer Guide

## Quick Start

### Environment Prerequisites
1. Node.js >= 16
2. Python >= 3.8
3. Git

### Clone Project
```bash
git clone <repository-url>
cd c2
```

### Frontend Development
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### Backend Development
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env file with necessary configurations

# Start development server
python run.py
```

## Project Structure

### Frontend Structure
```
frontend/
├── src/                # Source code directory
│   ├── api.ts         # API interface encapsulation
│   ├── App.vue        # Root component
│   ├── main.ts        # Entry file
│   ├── router/        # Router configuration
│   └── views/         # Page components
├── public/            # Static resources
└── vite.config.ts     # Vite configuration
```

### Backend Structure
```
backend/
├── src/              # Source code directory
│   ├── api/         # API related code
│   │   ├── models/  # Data models
│   │   └── routers/ # Route handlers
│   ├── config/      # Configuration files
│   └── core/        # Core functionality
├── tests/           # Test code
└── run.py           # Entry file
```

## Development Standards

### Code Style
- Frontend follows TypeScript standard specifications
- Backend follows PEP 8 specifications
- Use ESLint and Prettier for code formatting
- Use Python Black for Python code formatting

### Git Commit Standards
```
feat: new feature
fix: bug fix
docs: documentation update
style: code format (changes that don't affect code execution)
refactor: refactoring (code changes that are neither new features nor bug fixes)
perf: performance optimization
test: add tests
chore: build process or auxiliary tool changes
```

### Branch Management
- main: production branch
- develop: development branch
- feature/*: feature branches
- hotfix/*: emergency fix branches

## Development Process

### 1. Feature Development
1. Create feature branch from develop
   ```bash
   git checkout develop
   git checkout -b feature/your-feature
   ```

2. Develop new feature
   - Write code
   - Write tests
   - Local testing

3. Commit code
   ```bash
   git add .
   git commit -m "feat: your feature description"
   ```

4. Push to remote
   ```bash
   git push origin feature/your-feature
   ```

5. Create Pull Request

### 2. Code Review
- Check code standards
- Run test cases
- Code review
- Handle feedback

### 3. Merge Code
- Merge to develop branch
- Delete feature branch

## Testing Guide

### Unit Testing
- Frontend uses Jest for unit testing
  ```bash
  cd frontend
  npm run test:unit
  ```

- Backend uses pytest for unit testing
  ```bash
  cd backend
  python -m pytest tests/
  ```

### End-to-End Testing
- Using Cypress for E2E testing
  ```bash
  cd frontend
  npm run test:e2e
  ```

## Common Issues

### 1. Environment Configuration Issues
- Check Node.js version
- Check Python version
- Confirm all dependencies are installed
- Verify environment variable configuration

### 2. API Call Issues
- Check API address configuration
- Confirm request method and parameters
- Check network request logs
- Verify authentication information

### 3. Database Connection Issues
- Check database configuration
- Confirm database service status
- Verify connection string
- Check user permissions

## Security Considerations

### 1. Authentication & Authorization
- JWT Token validation
- Role-based access control
- Request signature verification

### 2. Data Security
- Use HTTPS
- Encrypted data storage
- XSS protection
- CSRF protection

### 3. Service Security
- Rate limiting
- DDoS protection
- Log auditing
- Backup strategy

## Performance Optimization

### Frontend Optimization
1. Code splitting
2. Lazy loading components
3. Caching strategy
4. Resource compression

### Backend Optimization
1. Database index optimization
2. Cache utilization
3. Asynchronous processing
4. Load balancing