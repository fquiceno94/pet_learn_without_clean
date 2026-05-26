import pandera.pandas as pa
from pandera.typing import Series
import pandas as pd

class RawMarketSchema(pa.DataFrameModel):
    id: Series[str]
    conditionId: Series[str]
    outcomePrices: Series[str] = pa.Field(nullable=True)
    active: Series[bool]
    closed: Series[bool]
    volume: Series[str] = pa.Field(nullable=True)

def validate_raw_markets(raw: list[dict])-> list[dict]:
    df = pd.DataFrame(raw)
    validated = RawMarketSchema.validate(df)

    return (
        validated
        .astype(object)
        .where(pd.notnull(validated), other=None)
        .to_dict(orient="records")
    )