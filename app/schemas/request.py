from pydantic import BaseModel, Field
from typing import Any, Dict, Optional


class UserRequest(BaseModel):
    user_id: str = Field(..., description="用户ID")
    message: str = Field(..., description="用户输入内容")


class IntentResult(BaseModel):
    intent_type: str
    confidence: float = 0.0
    raw_text: str
    fallback_response: str = "已收到您的消息，正在处理中。"
    detail: Dict[str, Any] = {}


class AgentResponse(BaseModel):
    response: str
    detail: Dict[str, Any] = {}


class SentimentResult(BaseModel):
    sentiment: str
    score: float
    response: str
    detail: Dict[str, Any] = {}


class ChatResponse(BaseModel):
    success: bool
    intent: str
    response: str
    trace_id: str
    detail: Dict[str, Any] = {}
