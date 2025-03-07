from typing import List, Dict, Optional
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class OpenAIService:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1"),  # 可以配置自定义基础URL
        )
        self.model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")  # 默认使用 gpt-3.5-turbo
        
    async def create_chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> Dict:
        """
        创建聊天完成请求
        Args:
            messages: 消息历史列表
            temperature: 温度参数(0-1)，控制响应的随机性
            max_tokens: 最大token数限制
        Returns:
            Dict: OpenAI的响应
        """
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=False
            )
            return {
                "content": response.choices[0].message.content,
                "role": "assistant",
                "tokens": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                }
            }
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")
            
    async def create_streaming_chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ):
        """
        创建流式聊天完成请求
        Args:
            messages: 消息历史列表
            temperature: 温度参数(0-1)
            max_tokens: 最大token数限制
        Yields:
            str: 流式响应的文本片段
        """
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True
            )
            
            async for chunk in response:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")