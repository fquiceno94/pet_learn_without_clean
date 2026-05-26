from fastapi import FastAPI
from app.api.routes.markets import router

app = FastAPI()

app.include_router(router=router)