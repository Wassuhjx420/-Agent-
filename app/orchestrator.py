from app.agents.intent_agent import IntentAgent
from app.agents.aftersales_agent import AfterSalesAgent
from app.agents.sentiment_agent import SentimentAgent
from app.agents.inventory_agent import InventoryAgent
from app.agents.review_agent import ReviewAgent
from app.schemas.request import UserRequest, ChatResponse
from app.utils.trace import new_trace_id


class Orchestrator:
    def __init__(self):
        self.intent_agent = IntentAgent()
        self.aftersales_agent = AfterSalesAgent()
        self.sentiment_agent = SentimentAgent()
        self.inventory_agent = InventoryAgent()
        self.review_agent = ReviewAgent()

    async def handle(self, request: UserRequest) -> ChatResponse:
        trace_id = new_trace_id()

        intent_result = await self.intent_agent.run(
            message=request.message,
            user_id=request.user_id,
            trace_id=trace_id,
        )

        intent_type = intent_result.intent_type

        if intent_type == "aftersales":
            result = await self.aftersales_agent.run(
                context=intent_result,
                user_id=request.user_id,
                trace_id=trace_id,
            )
            return ChatResponse(
                success=True,
                intent=intent_type,
                response=result.response,
                trace_id=trace_id,
                detail=result.detail,
            )

        if intent_type == "complaint":
            sentiment = await self.sentiment_agent.run(
                text=request.message,
                trace_id=trace_id,
            )
            review = await self.review_agent.run(
                complaint_text=request.message,
                sentiment=sentiment.sentiment,
                trace_id=trace_id,
            )
            return ChatResponse(
                success=True,
                intent=intent_type,
                response=review.response,
                trace_id=trace_id,
                detail=review.detail,
            )

        if intent_type == "stock":
            inventory = await self.inventory_agent.run(
                text=request.message,
                trace_id=trace_id,
            )
            return ChatResponse(
                success=True,
                intent=intent_type,
                response=inventory.response,
                trace_id=trace_id,
                detail=inventory.detail,
            )

        if intent_type == "query":
            return ChatResponse(
                success=True,
                intent=intent_type,
                response=intent_result.fallback_response,
                trace_id=trace_id,
                detail=intent_result.detail,
            )

        return ChatResponse(
            success=True,
            intent="handoff",
            response="当前问题超出自动处理范围，已建议转人工兜底。",
            trace_id=trace_id,
            detail={"reason": "out_of_scope"},
        )
