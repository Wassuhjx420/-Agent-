# 电商全链路智能运营多 Agent 系统



- 意图识别 Agent
- 售后工单处理 Agent
- 舆情分析 Agent
- 库存联动 Agent
- 运营复盘 Agent
- FastAPI API 入口
- Claude / 大模型调用封装
- 模拟订单、物流、评论等服务层



## 目录结构

```bash
ecom_multi_agent_system/
├── app/
│   ├── main.py
│   ├── orchestrator.py
│   ├── agents/
│   ├── services/
│   ├── schemas/
│   └── utils/
├── requirements.txt
├── .gitignore
├── .env.example
└── README.md
```

## 快速启动

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

复制一份环境变量文件：

```bash
cp .env.example .env
```

填入你的 Claude API Key。

### 3. 启动服务

```bash
uvicorn app.main:app --reload
```

### 4. 调用接口

```bash
curl -X POST "http://127.0.0.1:8000/chat"   -H "Content-Type: application/json"   -d '{"user_id":"u10086","message":"我的快递还没到，帮我查一下"}'
```

## 示例接口

### POST `/chat`

请求体：

```json
{
  "user_id": "u10086",
  "message": "我的订单什么时候发货？"
}
```

返回示例：

```json
{
  "success": true,
  "intent": "aftersales",
  "response": "订单已查到，当前状态为待发货，预计 24 小时内发出。",
  "trace_id": "..."
}
```

## 后续可扩展方向

- 接入 Redis 保存上下文
- 接入 Celery 做舆情抓取任务
- 接入 PostgreSQL / ClickHouse 存储业务数据
- 接入真实订单、物流、售后规则、库存和舆情平台
- 使用 LangGraph / AutoGen 做更复杂的 Agent 编排

## 免责声明

当前代码中的订单、物流、舆情、库存逻辑均为演示版模拟实现，生产环境需要替换为真实系统接口。
