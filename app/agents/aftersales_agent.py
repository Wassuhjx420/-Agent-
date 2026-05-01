from app.schemas.request import AgentResponse, IntentResult
from app.services.order_service import get_order_by_user
from app.services.logistics_service import get_logistics_by_order
from app.services.llm import decide_aftersales_action


class AfterSalesAgent:
    async def run(self, context: IntentResult, user_id: str, trace_id: str) -> AgentResponse:
        order = await get_order_by_user(user_id=user_id)
        logistics = await get_logistics_by_order(order_id=order["order_id"])
        decision = await decide_aftersales_action(
            user_message=context.raw_text,
            order=order,
            logistics=logistics,
            trace_id=trace_id,
        )

        return AgentResponse(
            response=decision["response"],
            detail={
                "order": order,
                "logistics": logistics,
                "decision": decision["decision"],
            },
        )
