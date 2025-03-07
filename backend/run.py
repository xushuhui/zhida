import uvicorn
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()

if __name__ == "__main__":
    uvicorn.run(
        "src.api.main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=True
    )