import uvicorn
from src.api.main import app
from src.core.database import init_db

if __name__ == "__main__":
    # Initialize the database
    init_db()
    
    # Start the FastAPI application
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True
    )