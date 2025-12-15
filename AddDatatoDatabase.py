import sqlite3
from datetime import datetime

# 1. Connect to database
conn = sqlite3.connect('database.db')
c = conn.cursor()

# 2. Create the table
c.execute("""CREATE TABLE IF NOT EXISTS students (
            id TEXT PRIMARY KEY,
            name TEXT,
            major TEXT,
            starting_year INTEGER,
            total_attendance INTEGER,
            standing TEXT,
            year INTEGER,
            last_attendance_time TEXT
            )""")

# 3. Your Specific Data
# Note: I assumed 'Year' is 4 based on 2022 start date, and 'Standing' is 'G' (Good).
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

data = [
    (
        "2231205042",           # ID
        "Muhtasim Rasheed",     # Name
        "CSE",                  # Major
        2022,                   # Starting Year
        20,                     # Total Attendance
        "G",                    # Standing (Default: G)
        4,                      # Year (Default: 4)
        current_time            # Last Attendance Time
    ),
    (
        "2211203042",           # ID
        "Isnat Hossain Rijon",  # Name
        "CSE",                  # Major
        2022,                   # Starting Year
        20,                     # Total Attendance
        "G",                    # Standing (Default: G)
        4,                      # Year (Default: 4)
        current_time            # Last Attendance Time
    ),
(
        "2211138642",           # ID
        "Syed Mahi Ashrafi",    # Name
        "CSE",                  # Major
        2022,                   # Starting Year
        18,                     # Total Attendance
        "G",                    # Standing (Default: G)
        4,                      # Year (Default: 4)
        current_time            # Last Attendance Time
    ),
(
        "2132418042",           # ID
        "Fardeen Abdullah Taseen",  # Name
        "CSE",                  # Major
        2022,                   # Starting Year
        15,                     # Total Attendance
        "G",                    # Standing (Default: G)
        4,                      # Year (Default: 4)
        current_time            # Last Attendance Time
    )
]

# 4. Insert Data
# 'INSERT OR REPLACE' updates the user if they already exist, so you can run this script multiple times to reset data.
c.executemany("INSERT OR REPLACE INTO students VALUES (?, ?, ?, ?, ?, ?, ?, ?)", data)

conn.commit()
conn.close()
print("Database created successfully!")