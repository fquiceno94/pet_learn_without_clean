from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from app.models.market import MarketModel

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
