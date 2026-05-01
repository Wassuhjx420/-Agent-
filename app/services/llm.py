import os
from typing import Any, Dict


async def classify_intent(message: str, user_id: str, trace_id: str) -> Dict[str, Any]:
    text = message.lower()

    if any(k in text for k in ["退款", "退货", "换货", "售后", "赔付", "发货", "快递", "物流"]):
        return {
            "intent_type": "aftersales",
            "confidence": 0.96,
            "fallback_response": "我先帮您处理售后问题。",
            "detail": {"trace_id": trace_id, "user_id": user_id},
        }

    if any(k in text for k in ["差评", "投诉", "不好", "很差", "舆情", "吐槽"]):
        return {
            "intent_type": "complaint",
            "confidence": 0.93,
            "fallback_response": "已记录您的反馈，正在分析问题。",
            "detail": {"trace_id": trace_id, "user_id": user_id},
        }

    if any(k in text for k in ["库存", "缺货", "补货", "sku", "货量"]):
        return {
            "intent_type": "stock",
            "confidence": 0.90,
            "fallback_response": "正在检查库存状态。",
            "detail": {"trace_id": trace_id, "user_id": user_id},
        }

    return {
        "intent_type": "query",
        "confidence": 0.80,
        "fallback_response": "我先帮您查询一下商品信息。",
        "detail": {"trace_id": trace_id, "user_id": user_id},
    }


async def decide_aftersales_action(user_message: str, order: Dict[str, Any], logistics: Dict[str, Any], trace_id: str) -> Dict[str, Any]:
    if logistics["status"] == "in_transit":
        return {
            "decision": "track_package",
            "response": f"订单 {order['order_id']} 已在运输中，当前物流状态：{logistics['status_text']}，预计 {logistics['eta']} 内送达。",
            "detail": {"trace_id": trace_id},
        }

    if logistics["status"] == "pending":
        return {
            "decision": "wait_and_notify",
            "response": f"订单 {order['order_id']} 当前待发货，预计 {logistics['eta']} 内发出。",
            "detail": {"trace_id": trace_id},
        }

    return {
        "decision": "human_handoff",
        "response": f"订单 {order['order_id']} 已进入人工兜底流程，我已为您发起转人工。",
        "detail": {"trace_id": trace_id},
    }


async def analyze_sentiment(text: str, trace_id: str) -> Dict[str, Any]:
    negative_keywords = ["差", "慢", "坏", "投诉", "失望", "退货", "垃圾"]
    score = 0.2 if any(k in text for k in negative_keywords) else 0.8
    sentiment = "negative" if score < 0.5 else "positive"
    response = "已识别为负面反馈，建议同步运营复盘。" if sentiment == "negative" else "反馈已记录，情绪正常。"
    return {
        "sentiment": sentiment,
        "score": score,
        "response": response,
        "detail": {"trace_id": trace_id},
    }


async def generate_review_report(complaint_text: str, sentiment: str, trace_id: str) -> Dict[str, Any]:
    if sentiment == "negative":
        response = "已生成负面舆情复盘：建议优先优化物流时效、售后响应和商品描述一致性。"
    else:
        response = "已生成常规复盘报告：当前用户反馈整体正常。"
    return {
        "response": response,
        "detail": {"trace_id": trace_id, "sentiment": sentiment},
    }
