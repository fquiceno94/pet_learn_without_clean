import json
from datetime import datetime

def transform_market(raw: dict) -> dict:

    
    return {
       
        "id": raw["id"],
        "condition_id": raw["conditionId"],
        "question": raw["question"],
        "slug": raw["slug"],
        "start_date": datetime.fromisoformat(raw["startDate"].replace("Z", "+00:00")) if raw.get("startDate") else None,
        "end_date": datetime.fromisoformat(raw["endDate"].replace("Z", "+00:00")) if raw.get("endDate") else None,
        "outcome_prices": [float(x) for x in json.loads(raw["outcomePrices"])] if raw.get("outcomePrices") else None,
        "volume": float(raw["volume"]) if raw.get("volume") is not None else None,
        "volume_24hr": float(raw["volume24hr"]) if raw.get("volume24hr") is not None else None,
        "liquidity": float(raw["liquidityNum"]) if raw.get("liquidityNum") is not None else None,
        "active": raw["active"],
        "closed": raw["closed"],
        "tags": raw.get("tags"),
        "clob_token_ids": [str(x) for x in json.loads(raw["clobTokenIds"])] if raw.get("clobTokenIds") else None,
        "event_slug": raw["events"][0]["slug"] if raw.get("events") else None,
    }
