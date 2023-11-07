import sqlite3

# Define the SQLite database file name
db_file = 'YT_database.db'

# Create a connection to the database (or create a new database if it doesn't exist)
conn = sqlite3.connect(db_file)

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create a Songs table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Songs (
        song_id INTEGER PRIMARY KEY,
        title TEXT,
        author TEXT,
        views INTEGER,
        length INTEGER,
        publish_date TEXT,
        link TEXT
    )
''')

# Create an Artists table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Artists (
        artist_id INTEGER PRIMARY KEY,
        name TEXT
    )
''')

# Create the Song-Artist Relationship Table (Many-to-Many)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS SongArtist (
        relation_id INTEGER PRIMARY KEY,
        song_id INTEGER,
        artist_id INTEGER,
        FOREIGN KEY (song_id) REFERENCES Songs (song_id),
        FOREIGN KEY (artist_id) REFERENCES Artists (artist_id)
    )
''')

# Commit the changes and close the database connection
conn.commit()
conn.close()

print("Database and tables have been created.")

