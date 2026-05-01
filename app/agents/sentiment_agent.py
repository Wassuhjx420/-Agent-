from app.schemas.request import SentimentResult
from app.services.llm import analyze_sentiment


class SentimentAgent:
    async def run(self, text: str, trace_id: str) -> SentimentResult:
        result = await analyze_sentiment(text=text, trace_id=trace_id)
        return SentimentResult(
            sentiment=result["sentiment"],
            score=result["score"],
            response=result["response"],
            detail=result.get("detail", {}),
        )
