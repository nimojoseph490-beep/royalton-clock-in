import sqlite3

# 1. Connect to (or create) the database file
connection = sqlite3.connect('royalton_school.db')
cursor = connection.cursor()

# 2. Create a table to store clock-in data
# We store Name, ID, Date, and Time
cursor.execute('''
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT,
        student_name TEXT,
        date TEXT,
        time TEXT
    )
''')

connection.commit()
connection.close()

print("✅ Database 'royalton_school.db' created successfully!")