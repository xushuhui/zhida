import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.database import engine, SessionLocal, init_db
from src.models.base import Base, User
from src.repositories import UserRepository
from src.api.utils.auth import get_password_hash
from sqlalchemy.sql import text

def test_connection():
    """Test database connection and create test user"""
    try:
        db = SessionLocal()
        print("Successfully connected to database")

        # Initialize database tables
        init_db()
        print("Database tables created")

        # Create test user if not exists
        user_repo = UserRepository(db)
        test_user = user_repo.get_by_username("test")
        if not test_user:
            test_user = user_repo.create({
                "username": "test",
                "email": "test@example.com",
                "password": get_password_hash("test123"),
                "role": "admin",
                "status": "active"
            })
            print("Created test user: test/test123")
        else:
            print("Test user already exists")

        db.close()
        print("Database connection test completed successfully")

    except Exception as e:
        print(f"Error testing database connection: {str(e)}")
        raise

if __name__ == "__main__":
    test_connection()