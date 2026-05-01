from app.schemas.request import IntentResult
from app.services.llm import classify_intent


class IntentAgent:
    async def run(self, message: str, user_id: str, trace_id: str) -> IntentResult:
        result = await classify_intent(message=message, user_id=user_id, trace_id=trace_id)
        return IntentResult(
            intent_type=result["intent_type"],
            confidence=result["confidence"],
            raw_text=message,
            fallback_response=result.get("fallback_response", "我先帮您记录一下，稍后继续处理。"),
            detail=result.get("detail", {}),
        )
