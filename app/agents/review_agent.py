from app.schemas.request import AgentResponse
from app.services.llm import generate_review_report


class ReviewAgent:
    async def run(self, complaint_text: str, sentiment: str, trace_id: str) -> AgentResponse:
        result = await generate_review_report(
            complaint_text=complaint_text,
            sentiment=sentiment,
            trace_id=trace_id,
        )
        return AgentResponse(
            response=result["response"],
            detail=result.get("detail", {}),
        )
