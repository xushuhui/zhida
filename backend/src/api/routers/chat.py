from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..models.chat import MessageCreate, SessionCreate, Message, Session, ChatResponse
from ..routers.auth import get_current_user
from ...core.database import get_db
from ...models.base import User as UserModel
from ...models.base import Session as SessionModel
from ...models.base import Message as MessageModel
from ...services.openai_service import OpenAIService

router = APIRouter()
openai_service = OpenAIService()

@router.post("/sessions", response_model=Session)
async def create_session(
    session: SessionCreate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_session = SessionModel(
        user_id=current_user.id,
        title=session.title or "New Chat",
        status="active",
        message_count=0,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        context={}
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

@router.get("/sessions", response_model=List[Session])
async def get_sessions(
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(SessionModel).filter(
        SessionModel.user_id == current_user.id
    ).order_by(SessionModel.updated_at.desc()).all()

@router.get("/sessions/{session_id}", response_model=Session)
async def get_session(
    session_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    session = db.query(SessionModel).filter(
        SessionModel.id == session_id,
        SessionModel.user_id == current_user.id
    ).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    return session

@router.post("/sessions/{session_id}/messages", response_model=ChatResponse)
async def create_message(
    session_id: int,
    message: MessageCreate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    session = db.query(SessionModel).filter(
        SessionModel.id == session_id,
        SessionModel.user_id == current_user.id
    ).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )

    start_time = datetime.utcnow()
    
    # Create user message
    user_message = MessageModel(
        session_id=session_id,
        user_id=current_user.id,
        role="user",
        content=message.content,
        status="sent",
        created_at=start_time
    )
    db.add(user_message)
    
    # Update session
    session.message_count += 1
    session.last_message_time = start_time
    session.updated_at = start_time
    
    # Get conversation history
    history = db.query(MessageModel).filter(
        MessageModel.session_id == session_id
    ).order_by(MessageModel.created_at.asc()).all()
    
    # Format messages for OpenAI
    messages = [{"role": msg.role, "content": msg.content} for msg in history]
    messages.append({"role": "user", "content": message.content})
    
    try:
        # Get response from OpenAI
        response = await openai_service.create_chat_completion(messages)
        end_time = datetime.utcnow()
        response_time = (end_time - start_time).total_seconds()
        
        # Create assistant message
        assistant_message = MessageModel(
            session_id=session_id,
            user_id=current_user.id,
            role="assistant",
            content=response["content"],
            status="sent",
            created_at=end_time,
            response_time=response_time,
            tokens=response["tokens"]["total_tokens"],
            metadata={
                "prompt_tokens": response["tokens"]["prompt_tokens"],
                "completion_tokens": response["tokens"]["completion_tokens"],
                "model": openai_service.model
            }
        )
        db.add(assistant_message)
        
        # Increment message count for assistant message
        session.message_count += 1
        
        db.commit()
        db.refresh(user_message)
        db.refresh(assistant_message)
        
        return ChatResponse(
            response=response["content"],
            session_id=session_id,
            messages=[user_message, assistant_message]
        )
        
    except Exception as e:
        # In case of error, still save the user message but mark it as error
        user_message.status = "error"
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/sessions/{session_id}/messages", response_model=List[Message])
async def get_messages(
    session_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify session belongs to user
    session = db.query(SessionModel).filter(
        SessionModel.id == session_id,
        SessionModel.user_id == current_user.id
    ).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    messages = db.query(MessageModel).filter(
        MessageModel.session_id == session_id
    ).order_by(MessageModel.created_at.asc()).all()
    
    return messages

@router.delete("/sessions/{session_id}")
async def delete_session(
    session_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    session = db.query(SessionModel).filter(
        SessionModel.id == session_id,
        SessionModel.user_id == current_user.id
    ).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    # Delete all messages in the session
    db.query(MessageModel).filter(MessageModel.session_id == session_id).delete()
    
    # Delete the session
    db.delete(session)
    db.commit()
    
    return {"status": "success", "message": "Session deleted"}