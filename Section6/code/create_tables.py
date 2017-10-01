import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
# int - a random integer
# INTEGER PRIMARY KEY - allows for auto incrementing ID

create_item_table = "CREATE TABLE IF NOT EXISTS items (name text, price real)" 

cursor.execute(create_table)
cursor.execute(create_item_table)

connection.commit()
connection.close()