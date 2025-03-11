from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, JSON, Enum, ForeignKey, Text, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    avatar = Column(String(255))
    role = Column(Enum('admin', 'user', name='user_roles'), default='user', nullable=False)
    status = Column(Enum('active', 'disabled', name='user_status'), default='active', nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_login = Column(DateTime)
    preferences = Column(JSON)

    sessions = relationship("Session", back_populates="user", cascade="all, delete-orphan")
    messages = relationship("Message", back_populates="user", cascade="all, delete-orphan")
    statistics = relationship("Statistics", back_populates="user", cascade="all, delete-orphan")

class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    title = Column(String(255), nullable=False)
    status = Column(Enum('active', 'archived', name='session_status'), default='active', nullable=False)
    message_count = Column(Integer, default=0)
    last_message_time = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    system_prompt = Column(Text)
    temperature = Column(Float(2))
    max_tokens = Column(Integer)

    user = relationship("User", back_populates="sessions")
    messages = relationship("Message", back_populates="session", cascade="all, delete-orphan")

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey('sessions.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    role = Column(Enum('user', 'assistant', 'system', name='message_roles'), nullable=False)
    content = Column(Text, nullable=False)
    tokens = Column(Integer)
    status = Column(Enum('sent', 'delivered', 'error', name='message_status'), default='sent', nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    response_time = Column(Integer)
    client_info = Column(String(255))
    ip_address = Column(String(45))

    session = relationship("Session", back_populates="messages")
    user = relationship("User", back_populates="messages")

class Statistics(Base):
    __tablename__ = "statistics"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    date = Column(DateTime, nullable=False)
    chat_count = Column(Integer, default=0)
    message_count = Column(Integer, default=0)
    avg_response_time = Column(Float)
    token_usage = Column(Integer, default=0)
    error_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="statistics")