from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from app.models.market import MarketModel
from sqlalchemy import select

async def upsert_markets(session: AsyncSession,markets: list[dict]) -> int:

    BATCH_SIZE = 500 # 500*13 = 6500 params
    
    for i in range(0, len(markets),BATCH_SIZE):
        batch = markets[i:i + BATCH_SIZE]
        stmt = insert(MarketModel).values(batch)
        stmt = stmt.on_conflict_do_update(
            index_elements=["id"],
            set_={col.name: stmt.excluded[col.name] for col in MarketModel.__table__.columns if col.name != "id"}

        )

        await session.execute(stmt)
    await session.commit()

    return len(markets)

async def get_active_markets(session: AsyncSession, limit: int, offset: int) -> list[MarketModel]:
    
    result = await session.execute(
    select(MarketModel)
    .where(MarketModel.active == True)
    .order_by(MarketModel.volume.desc())
    .limit(limit)
    .offset(offset)
    )

    return result.scalars().all()

async def get_market_by_id(session: AsyncSession, id: str):

    result = await session.execute(
        select(MarketModel)
        .where(MarketModel.id == id)
    )
    return result.scalars().first()