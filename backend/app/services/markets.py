from app.ingestion.polymarket.gamma_client import GammaClient
from app.ingestion.polymarket.transformer import transform_market
from app.repositories.markets import upsert_markets
from sqlalchemy.ext.asyncio import AsyncSession
from app.ingestion.polymarket.schemas import validate_raw_markets
import logging

logger = logging.getLogger(__name__)

async def ingest_markets(session: AsyncSession)-> int:

    raw_markets = await GammaClient().fetch_active_markets()
    raw_markets = validate_raw_markets(raw_markets)

    logger.info(f"Mercados obtenidos de la API: {len(raw_markets)}")
    
    transformed = [transform_market(m) for m in raw_markets if m.get("outcomePrices")]

    logger.info(f"Mercados con outcomePrices: {len(transformed)}")
    logger.info(f"Descartados sin outcomePrices: {len(raw_markets) - len(transformed)}")
    
    count = await upsert_markets(session, transformed)
    logger.info(f"Mercados guardados en DB: {count}")

    return count