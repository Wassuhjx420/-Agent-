from app.schemas.request import AgentResponse
from app.services.inventory_service import inspect_inventory_risk


class InventoryAgent:
    async def run(self, text: str, trace_id: str) -> AgentResponse:
        result = await inspect_inventory_risk(text=text, trace_id=trace_id)
        return AgentResponse(
            response=result["response"],
            detail=result.get("detail", {}),
        )
