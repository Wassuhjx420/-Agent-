from typing import Dict


async def get_order_by_user(user_id: str) -> Dict:
    return {
        "user_id": user_id,
        "order_id": "OD202506010001",
        "sku": "SKU-CHILL-001",
        "status": "pending",
        "amount": 199.0,
    }
