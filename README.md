# 知答 (Knowledge Answer)

知答 is a modern customer service solution developed with Vue 3 and FastAPI, integrating OpenAI GPT models to provide intelligent conversation services.

## Features

### Currently Implemented
- User Authentication
  - User login/logout
  - JWT Token authentication
  - Session management
- Chat Features
  - Real-time text conversation
  - Multi-session management
  - Markdown message rendering
  - History viewing
- Data Statistics
  - Conversation count statistics
  - Message count statistics
  - Response time statistics
  - Satisfaction statistics

### Planned Features
- User management functionality
- Knowledge base management
- Data analysis reports
- System monitoring dashboard

## Technology Stack

### Frontend
- Vue 3 + TypeScript
- Element Plus
- Vite
- WebSocket
- Jest + Cypress

### Backend
- Python FastAPI
- MySQL
- Redis
- OpenAI API
- pytest

## Quick Start

### Prerequisites
- Node.js >= 16
- Python >= 3.8
- MySQL >= 8.0
- Redis >= 6.2

### Development Setup
1. Clone the repository
```bash
git clone <repository-url>
cd zhida
```

2. Frontend setup
```bash
cd frontend
npm install
npm run dev
```

3. Backend setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\\venv\\Scripts\\activate  # Windows
pip install -r requirements.txt
python run.py
```

## Documentation
- [Requirements](docs/requirements.md) - Detailed functional and non-functional requirements
- [Technical Design](docs/technical-design.md) - System architecture and technical implementation details
- [API Documentation](docs/api.md) - API specifications and usage instructions
- [Deployment Guide](docs/deployment.md) - Environment configuration and deployment guide
- [Developer Guide](docs/developer-guide.md) - Development process and specifications
- [Testing Documentation](docs/testing.md) - Test plans and case descriptions
- [Database Design](docs/database.md) - Database structure and optimization
- [Product Introduction](docs/product.md) - Product features and advantages

## Directory Structure
```
.
├── frontend/           # Frontend Vue application
│   ├── src/           # Source code
│   ├── public/        # Static assets
│   └── tests/         # Test files
├── backend/           # Backend FastAPI application
│   ├── src/          # Source code
│   ├── tests/        # Test files
│   └── migrations/   # Database migrations
├── docs/             # Documentation
│   ├── api.md        # API documentation
│   ├── deployment.md # Deployment guide
│   └── ...          # Other docs
├── assets/           # Resource files
│   └── images/      # Image resources
├── docker-compose.yml # Docker configuration
└── README.md         # Project overview
```

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Support
- Documentation: https://docs.example.com
- Issue Tracker: https://github.com/example/zhida/issues
- Community Forum: https://forum.example.com
- Email: support@example.com