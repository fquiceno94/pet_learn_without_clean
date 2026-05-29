from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import func, Float, DateTime, Text
from sqlalchemy.dialects.postgresql import JSONB, ARRAY
from app.models.base import Base


class MarketModel(Base):
    __tablename__ = "markets"

    id: Mapped[str] = mapped_column(primary_key=True)
    condition_id: Mapped[str]
    question: Mapped[str]
    slug: Mapped[str]
    start_date: Mapped[Optional[datetime]]= mapped_column(DateTime(timezone=True),nullable=True)
    end_date: Mapped[Optional[datetime]]= mapped_column(DateTime(timezone=True),nullable=True)
    outcome_prices: Mapped[list[float]]= mapped_column(ARRAY(Float))
    volume: Mapped[Optional[float]] = mapped_column(nullable=True)
    volume_24hr:Mapped[Optional[float]]= mapped_column(nullable=True)
    liquidity: Mapped[Optional[float]]= mapped_column(nullable=True)
    active: Mapped[bool]
    closed: Mapped[bool]
    tags: Mapped[Optional[dict]]= mapped_column(JSONB,nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now())
    updated_at: Mapped[datetime]= mapped_column(DateTime(timezone=True),server_default=func.now(),onupdate=func.now())
    clob_token_ids: Mapped[Optional[list[str]]]= mapped_column(ARRAY(Text),nullable=True)
    event_slug: Mapped[Optional[str]]= mapped_column(nullable=True)