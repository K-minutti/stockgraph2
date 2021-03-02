import sqlite3
import os
import alpaca_trade_api as tradeapi
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv('ALPACA_API_KEY')
SECRET_KEY = os.getenv('ALPACA_API_SECRET')

connection = sqlite3.connect('app.db')

cursor = connection.cursor()

api = tradeapi.REST(API_KEY, SECRET_KEY, base_url='https://paper-api.alpaca.markets')
assets = api.list_assets()

for asset in assets:
    try:
        if asset.status == 'active' and asset.tradable:
            cursor.execute("""
                INSERT INTO stock (symbol, name, exchange)
                VALUES (?, ?, ?)
            """, (asset.symbol, asset.name, asset.exchange))
    except Exception as e:
        print(e)
        print(asset)

connection.commit()




