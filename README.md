# ZhiDa (Knowledge Answer)
An intelligent Q&A system based on Vue 3 + FastAPI, providing GPT-based intelligent conversation services.

## Project Structure
```
.
├── backend/             # Backend project directory
│   ├── src/            # Source code
│   ├── requirements.txt # Python dependencies
│   └── run.py          # Startup script
├── frontend/           # Frontend project directory
│   ├── src/           # Source code
│   └── package.json   # Project dependencies
└── docs/              # Project documentation
    ├── api.md             # API documentation
    ├── deployment.md      # Deployment guide
    ├── developer-guide.md # Development guide
    ├── product.md         # Product introduction
    ├── requirements.md    # Requirements documentation
    └── technical-design.md # Technical design
    └── testing.md         # Testing documentation
```

## Development Environment Requirements
- Node.js >= 16
- Python >= 3.8
- OpenAI API Key

## Quick Start
1. Start backend service:
```bash
# Enter backend directory
cd backend
# Install dependencies
pip install -r requirements.txt
# Configure environment variables
cp .env.example .env
# Edit .env file to set necessary environment variables
# Start service
python run.py
```

2. Start frontend service:
```bash
# Enter frontend directory
cd frontend
# Install dependencies
npm install
# Start development server
npm run dev
```

After services start:
- Frontend access: http://localhost:3000
- Backend API: http://localhost:8000

## Default User
System preset administrator account:
- Username: admin
- Password: secret

## Documentation
- [Requirements](docs/requirements.md) - Detailed functional and non-functional requirements
- [Technical Design](docs/technical-design.md) - System architecture and technical implementation details
- [API Documentation](docs/api.md) - API specifications and usage instructions
- [Deployment Guide](docs/deployment.md) - Environment configuration and deployment guide
- [Developer Guide](docs/developer-guide.md) - Development process and specifications
- [Testing Documentation](docs/testing.md) - Test plans and case descriptions
- [Product Introduction](docs/product.md) - Product features and advantages

## Currently Implemented Features
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

## Future Development Plans
- User management functionality
- Knowledge base management
- Data analysis reports
- System monitoring dashboard

## Complete Directory Structure
```
.
├── backend/             # Backend project directory
│   ├── src/            # Source code
│   │   ├── api/       # API related code
│   │   ├── config/    # Configuration files
│   │   └── models/    # Data models
│   ├── .env           # Environment variables
│   ├── .env.example   # Environment variables example
│   ├── requirements.txt # Python dependencies
│   └── run.py         # Startup script
├── frontend/           # Frontend project directory
│   ├── src/           # Source code
│   │   ├── api.ts     # API calls
│   │   ├── views/     # Page components
│   │   └── router/    # Route configuration
│   ├── package.json   # Project dependencies
│   └── vite.config.ts # Vite configuration
├── docs/              # Project documentation
│   ├── api.md             # API documentation
│   ├── deployment.md      # Deployment guide
│   ├── developer-guide.md # Development guide
│   ├── product.md         # Product introduction
│   ├── requirements.md    # Requirements documentation
│   └── technical-design.md # Technical design
│   └── testing.md         # Testing documentation
├── assets/            # Resource files
│   └── images/       # Image resources
├── .gitignore        # Git ignore configuration
└── README.md         # Project description
```