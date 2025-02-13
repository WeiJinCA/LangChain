import os
import sqlite3

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the database file path in the script's directory
db_path = os.path.join(script_dir, "langchain.db")

# Connect to the SQLite database (it will create the file if it doesn't exist)
connection = sqlite3.connect(db_path)
cursor = connection.cursor()

# # SQL to create the table
create_table_sql = """
CREATE TABLE full_llm_cache (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    prompt TEXT NOT NULL,
    response TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
"""

# Execute the SQL command
cursor.execute(create_table_sql)
# Commit changes and close the connection
connection.commit()

#Check if the table exists
# cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
# tables = cursor.fetchall()
# print("Tables in the database:", tables)

# if not any("full_llm_cache" in t for t in tables):
#     print("The table 'full_llm_cache' does not exist. Ensure it's created.")
# else:
#     print("The table 'full_llm_cache' exists!")


connection.close()

print(f"Table 'full_llm_cache' created successfully at {db_path}")