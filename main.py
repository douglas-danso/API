from fastapi import FastAPI, Query
import asyncio
import api  

app = FastAPI()

@app.get("/create")
async def create(
    email: str = Query(..., description="User email"), 
    password: str = Query(..., description="User password"),
    asset: str = Query(..., description="Asset symbol"),
    period: int = Query(60, description="Candle period in seconds", ge=1),  # Default 60 seconds
    offset: int = Query(100, description="Number of candles to fetch", ge=1)  # Default 100 candles
):
    fetcher = api.DataFetcher(email, password)
    await fetcher.start_fetching(asset, period, offset)  
    return {"message": "Quotex scraper started"}
