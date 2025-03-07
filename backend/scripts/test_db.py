import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.database import engine
from src.models.base import Base, User
from sqlalchemy.sql import text

def test_connection():
    try:
        # Test raw connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Database connection successful")
            
            # Test creating tables
            Base.metadata.create_all(engine)
            print("✅ Database tables created successfully")
            
            # Test basic query
            result = conn.execute(text("SHOW TABLES"))
            tables = [row[0] for row in result]
            print("📋 Available tables:", tables)
            
        return True
    except Exception as e:
        print("❌ Database connection failed:", str(e))
        return False

if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1)