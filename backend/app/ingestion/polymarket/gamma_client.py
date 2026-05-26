import httpx
from app.core.config import settings

class GammaClient():

    def __init__(self, base_url: str = settings.GAMMA_API_URL, limit: int= 100,timeout: float =  30.0):
        
        self.base_url = base_url
        self.limit = limit
        self.timeout = timeout

    async def fetch_active_markets(self) -> list[dict]:
        markets = []
        offset = 0
        async with httpx.AsyncClient(base_url=self.base_url, timeout=self.timeout) as client:
            while True:
                
                try:
                    response = await client.get("/markets",params={"closed": "false", "limit":self.limit, "offset": offset})
                    response.raise_for_status()
                    results = response.json()
                    markets.extend(results)

                    if len(results) < self.limit: break
                    offset += self.limit
                except httpx.HTTPStatusError as e:
                    if e.response.status_code == 422:
                        break
                    raise

        return markets

