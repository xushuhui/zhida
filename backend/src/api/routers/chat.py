from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from ..models.chat import ChatRequest, ChatResponse, Session, Message
from ..utils.auth import get_current_active_user
from ...core.database import get_db
from ...repositories import SessionRepository, MessageRepository, StatisticsRepository
from ...services.openai_service import OpenAIService
from ...config import settings

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: Request,
    chat_request: ChatRequest,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    session_repo = SessionRepository(db)
    message_repo = MessageRepository(db)
    stats_repo = StatisticsRepository(db)
    
    # Get or create session
    session = None
    if chat_request.session_id:
        session = session_repo.get(chat_request.session_id)
        if not session or session.user_id != current_user.id:
            raise HTTPException(status_code=404, detail="Session not found")
    
    if not session:
        # Create new session
        session = session_repo.create({
            "user_id": current_user.id,
            "title": chat_request.message[:50] + "...",
            "system_prompt": chat_request.system_prompt,
            "temperature": chat_request.temperature or settings.TEMPERATURE,
            "max_tokens": chat_request.max_tokens or settings.MAX_TOKENS
        })
    
    # Create user message
    start_time = datetime.utcnow()
    user_message = message_repo.create_message(
        session_id=session.id,
        user_id=current_user.id,
        role="user",
        content=chat_request.message,
        client_info=str(request.headers.get("user-agent")),
        ip_address=request.client.host
    )
    
    # Get chat completion from OpenAI
    openai_service = OpenAIService()
    system_prompt = chat_request.system_prompt or session.system_prompt
    temperature = chat_request.temperature or session.temperature or settings.TEMPERATURE
    max_tokens = chat_request.max_tokens or session.max_tokens or settings.MAX_TOKENS
    
    # Get chat history
    history = message_repo.get_session_messages(session.id)
    messages = [{"role": msg.role, "content": msg.content} for msg in history[-5:]]
    if system_prompt:
        messages.insert(0, {"role": "system", "content": system_prompt})
    
    try:
        response = await openai_service.get_chat_completion(
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        # Create assistant message
        end_time = datetime.utcnow()
        response_time = int((end_time - start_time).total_seconds() * 1000)
        
        assistant_message = message_repo.create_message(
            session_id=session.id,
            user_id=current_user.id,
            role="assistant",
            content=response.content,
            tokens=response.total_tokens,
            response_time=response_time
        )
        
        # Update session
        session_repo.update(session.id, {
            "message_count": session.message_count + 2,
            "last_message_time": end_time
        })
        
        # Update statistics
        stats_repo.update_daily_stats(
            user_id=current_user.id,
            stats_date=datetime.utcnow().date(),
            chat_count=1,
            message_count=2,
            avg_response_time=response_time,
            token_usage=response.total_tokens
        )
        
        return ChatResponse(
            session_id=session.id,
            message=assistant_message,
            total_tokens=response.total_tokens
        )
        
    except Exception as e:
        # Update statistics for error
        stats_repo.update_daily_stats(
            user_id=current_user.id,
            stats_date=datetime.utcnow().date(),
            error_count=1
        )
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sessions", response_model=List[Session])
async def list_sessions(
    skip: int = 0,
    limit: int = 20,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    session_repo = SessionRepository(db)
    return session_repo.get_user_sessions(current_user.id, skip, limit)

@router.get("/sessions/{session_id}", response_model=Session)
async def get_session(
    session_id: int,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    session_repo = SessionRepository(db)
    session = session_repo.get(session_id)
    if not session or session.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

@router.get("/sessions/{session_id}/messages", response_model=List[Message])
async def list_session_messages(
    session_id: int,
    skip: int = 0,
    limit: int = 50,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    session_repo = SessionRepository(db)
    message_repo = MessageRepository(db)
    
    session = session_repo.get(session_id)
    if not session or session.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Session not found")
        
    return message_repo.get_session_messages(session_id, skip, limit)

@router.post("/sessions/{session_id}/archive")
async def archive_session(
    session_id: int,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    session_repo = SessionRepository(db)
    session = session_repo.get(session_id)
    if not session or session.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Session not found")
        
    session_repo.archive_session(session_id)
    return {"status": "success"}