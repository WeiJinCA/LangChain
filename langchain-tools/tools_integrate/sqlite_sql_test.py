import sqlite3

# Path to your database
db_path = "/Users/weijin/Documents/code/Python/langchain-base/langchain-tools/tools_integrate/langchain.db"

connection = sqlite3.connect(db_path)
cursor = connection.cursor()

# Query to list all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("Tables in the database:", tables)

connection.close()