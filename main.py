from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
import asyncio
import os
import api  # Assuming api is the module containing DataFetcher

app = FastAPI()
app.get("/")
async def root():
    return {"message": "quotex api is live"}

@app.get("/create")
async def create(
    email: str = Query(..., description="User email"), 
    password: str = Query(..., description="User password"),
    asset: str = Query(..., description="Asset symbol"),
    period: int = Query(60, description="Candle period in seconds", ge=1),  # Default 60 seconds
    offset: int = Query(100, description="Number of candles to fetch", ge=1)  # Default 100 candles
):
    file_name = 'otc_data.csv'  
    
    fetcher = api.DataFetcher(email, password)
    await fetcher.fetch_and_save_data(asset, period, offset, file_name)

    # Check if file exists
    if os.path.exists(file_name):
        return FileResponse(file_name, media_type='text/csv', filename=file_name)
    else:
        return {"message": "File not found or data unavailable"}

