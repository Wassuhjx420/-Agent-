from typing import Dict


async def get_logistics_by_order(order_id: str) -> Dict:
    return {
        "order_id": order_id,
        "status": "pending",
        "status_text": "待发货",
        "eta": "24小时内",
        "carrier": "MockExpress",
    }
