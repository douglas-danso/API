from quotexpy import Quotex
import csv
import asyncio
from datetime import datetime
import os  # To check if file exists

class DataFetcher:
    def __init__(self, email, password):
        self.quotex = Quotex(email, password)

    async def fetch_and_save_data(self, asset, period, offset, file_name='otc_data.csv'):
        # Connect to the Quotex API
        await self.quotex.connect()
        print("Fetching candles data...")
        
        # Fetch candles data
        candles = await self.quotex.get_candle_v2(asset, period=period)
        print(candles)
        
        # Prepare the data in the correct format for CSV
        csv_data = [
            [datetime.fromtimestamp(candle['time']), candle['open'], candle['close'], candle['high'], candle['low']]
            for candle in candles
        ]
        
        # Check if the file already exists (to avoid overwriting headers)
        file_exists = os.path.isfile(file_name)
        
        # Open the CSV file in append mode
        with open(file_name, mode='a', newline='') as file:
            writer = csv.writer(file)
            
            # Write the header if the file is new
            if not file_exists:
                writer.writerow(["Time", "Open", "Close", "High", "Low"])
                
            # Append the data to the CSV file
            writer.writerows(csv_data)
        
        print(f"Data saved to {file_name}")

    async def start_fetching(self, asset, period, offset, interval=60, file_name='otc_data.csv'):
        # Periodically fetch and save data
        while True:
            await self.fetch_and_save_data(asset, period, offset, file_name)
            await asyncio.sleep(interval)  # Wait before the next fetch (60 seconds by default)



