from app.ingestion.polymarket.gamma_client import GammaClient
from app.ingestion.polymarket.transformer import transform_market
from app.repositories.markets import upsert_markets
from sqlalchemy.ext.asyncio import AsyncSession

async def ingest_markets(session: AsyncSession)-> int:

    raw_markets = await GammaClient().fetch_active_markets()
    transformed = [transform_market(m) for m in raw_markets if m.get("outcomePrices")]
    return await upsert_markets(session, transformed)