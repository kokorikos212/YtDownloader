import sqlite3

# Replace with your desired table name
name_table = "mytable"

# Connect to the SQLite database (it will create a new database if it doesn't exist)
conn = sqlite3.connect('Downloads_Database.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create the table if it doesn't already exist
cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS mytable(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        author TEXT,
        views INTEGER,
        length INTEGER,
        publish_date TEXT
    )
''')

# Commit the changes and close the connection
conn.commit()
conn.close()
