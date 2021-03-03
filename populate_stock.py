import sqlite3
import os
import alpaca_trade_api as tradeapi
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv('ALPACA_API_KEY')
SECRET_KEY = os.getenv('ALPACA_API_SECRET')

connection = sqlite3.connect('/Users/kevinminutti/Coding/stockgraph/app.db')
connection.row_factory = sqlite3.Row

cursor = connection.cursor()

cursor.execute("""
    SELECT symbol, name FROM stock
""")
rows = cursor.fetchall()

symbols = [row['symbol'] for row in rows] #current symbols in table

api = tradeapi.REST(API_KEY, SECRET_KEY, base_url='https://paper-api.alpaca.markets')
assets = api.list_assets()

for asset in assets:
    try:
        if asset.status == 'active' and asset.tradable and asset.symbol not in symbols:
            print(f"Added a new stock {asset.symbol} {asset.name}")
            cursor.execute("""
                INSERT INTO stock (symbol, name, exchange)
                VALUES (?, ?, ?)
            """, (asset.symbol, asset.name, asset.exchange))
    except Exception as e:
        print(e)
        print(asset)

connection.commit()

