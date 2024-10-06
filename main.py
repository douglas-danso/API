from fastapi import FastAPI, Query, WebSocket
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
    await fetcher.start_fetching(asset, period, offset, file_name)

    # Check if file exists
    if os.path.exists(file_name):
        return FileResponse(file_name, media_type='text/csv', filename=file_name)
    else:
        return {"message": "File not found or data unavailable"}



# @app.get("/create")
# async def create(
#     email: str = Query(..., description="User email"), 
#     password: str = Query(..., description="User password"),
#     asset: str = Query(..., description="Asset symbol"),
#     period: int = Query(60, description="Candle period in seconds", ge=1),  # Default 60 seconds
#     offset: int = Query(100, description="Number of candles to fetch", ge=1)  # Default 100 candles
# ):
#     fetcher = api.DataFetcher(email, pas  # No need for asyncio.run in FastAPI
#     return {"message": "Quotex scrapersword)
#     await fetcher.start_fetching(asset, period, offset) started"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, email: str, password: str, asset: str, period: int = 60, offset: int = 100):
    await websocket.accept() 
    
    # Instantiate DataFetcher with email and password
    fetcher = api.DataFetcher(email, password)
    
    try:
        # Periodically fetch and stream data over WebSocket in CSV format
        while True:
            print("Fetching data...")
            # Fetch data and get the CSV formatted string
            csv_string = await fetcher.start_fetching(asset, period, offset)
            
            if csv_string:
                print("Sending CSV data...")
                print(csv_string)
                await websocket.send_text(csv_string)  # Send CSV data as plain text
            else:
                print("No data to send")

            await asyncio.sleep(5)  # Send updates every 5 seconds
    except Exception as e:
        print(f"Error: {e}")
        await websocket.close()  # Close WebSocket connection if any error occurs
