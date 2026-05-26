from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, Depends, APIRouter
from app.repositories.markets import get_active_markets as fetch_markets, get_market_by_id as fetch_by_id
from app.schemas.markets import MarketResponse
from app.api.deps import get_db

router = APIRouter(prefix="/markets", tags=["markets"])

@router.get("/", response_model=list[MarketResponse])
async def get_active_markets(
    session: Annotated[AsyncSession, Depends(get_db)],
    limit: int = 50,
    offset: int =0
):
    return await fetch_markets(session=session,limit=limit,offset=offset)

@router.get("/{market_id}", response_model=MarketResponse)
async def get_market_by_id(
    market_id: str,
    session: Annotated[AsyncSession, Depends(get_db)]
):
    market = await fetch_by_id(session, market_id)
    if market is None:
        raise HTTPException(status_code=404, detail="El mercado no existe")
    return market