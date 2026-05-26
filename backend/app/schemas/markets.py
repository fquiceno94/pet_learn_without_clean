from pydantic import BaseModel, ConfigDict
from datetime import datetime

class MarketResponse(BaseModel):
    
    model_config = ConfigDict(from_attributes=True)

    id: str
    question: str
    slug: str
    start_date: datetime | None
    end_date: datetime | None
    outcome_prices: list[float] | None
    volume: float | None
    volume_24hr: float | None
    liquidity: float | None
    active: bool
    closed: bool

