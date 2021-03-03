import sqlite3

connection = sqlite3.connect('/Users/kevinminutti/Coding/stockgraph/app.db')

cursor = connection.cursor()

cursor.execute("""
    DROP TABLE stock_price
""")

cursor.execute(""" 
    DROP TABLE stock
""")

connection.commit()