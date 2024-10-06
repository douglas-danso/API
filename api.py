import csv
import asyncio
from datetime import datetime
import os
from quotexpy import Quotex
from quotexpy.utils.candles_period import CandlesPeriod
from quotexpy.utils import asset_parse
# from termcolor import colored

class DataFetcher:
    def __init__(self, email, password):
        self.quotex = Quotex(email, password)

    async def fetch_and_save_data(self, asset_current, offset, period=CandlesPeriod.ONE_MINUTE, file_name='otc_data.csv'):
        # Connect to the Quotex API
        await self.quotex.connect()
        print("Fetching candles data...")

        asset, asset_open = self.check_asset(asset_current)
        if asset_open[2]:
            print(("[INFO]: ", "blue"), "Asset is open.")
            candles = await self.quotex.get_candle_v2(asset,period )
            
        else:
            print(("[INFO]: ", "blue"), "Asset is closed.")

        # list_size = 10
        # asset, asset_open = self.check_asset(asset_current)
        # print("done checking")
        # self.quotex.start_candles_stream(asset, list_size)
        # print("starting stream")
        # # while True:
        # #     print("true")
        # #     if len(self.quotex.get_realtime_candles(asset)) == list_size:
        # #         break
        # candles = self.quotex.get_realtime_candles(asset)
        # # Prepare the data in the correct format for CSV
        csv_data = [
            [datetime.fromtimestamp(candle["time"]), candle["open"], candle["close"], candle["high"], candle["low"]]
            for candle in candles
        ]

        # Convert csv_data to a string format
        csv_string = ''
        csv_file_exists = os.path.isfile(file_name)

        # Open the CSV file in append mode and write data
        with open(file_name, mode='a', newline='') as file:
            writer = csv.writer(file)

            # Write the header if the file is new
            if not csv_file_exists:
                writer.writerow(["Time", "Open", "Close", "High", "Low"])

            # Write the rows to the file and generate the string version
            for row in csv_data:
                writer.writerow(row)
                csv_string += ','.join(map(str, row)) + '\n'

        print(f"Data saved to {file_name}")

        # Return the CSV string for WebSocket
        return csv_string

    async def start_fetching(self, asset, period, offset, interval=60, file_name='otc_data.csv'):
        # Periodically fetch and return the CSV data as a string
        csv_string = await self.fetch_and_save_data(asset, period, offset, file_name)
        return csv_string

    def check_asset(self,asset):
        asset_query = asset_parse(asset)
        asset_open = self.quotex.check_asset_open(asset_query)
        if not asset_open or not asset_open[2]:
            print(("[WARN]: ", "yellow"), "Asset is closed.")
            asset = f"{asset}_otc"
            print(("[WARN]: ", "yellow"), "Try OTC Asset -> " + asset)
            asset_query = asset_parse(asset)
            asset_open = self.quotex.check_asset_open(asset_query)
        return asset, asset_open

    # async def get_realtime_candle():
    # check_connect = await client.connect()
    # if check_connect:
    #     list_size = 10
    #     global asset_current
    #     asset, asset_open = check_asset(asset_current)
    #     client.start_candles_stream(asset, list_size)
    #     while True:
    #         if len(client.get_realtime_candles(asset)) == list_size:
    #             break
    #     print(client.get_realtime_candles(asset))


# async def get_candle_v2():
#     check_connect = await client.connect()
#     if check_connect:
#         global asset_current
#         asset, asset_open = check_asset(asset_current)
#         if asset_open[2]:
#             print(colored("[INFO]: ", "blue"), "Asset is open.")
#             candles = await client.get_candle_v2(asset, CandlesPeriod.ONE_MINUTE)
#             print(candles)
#         else:
#             print(colored("[INFO]: ", "blue"), "Asset is closed.")