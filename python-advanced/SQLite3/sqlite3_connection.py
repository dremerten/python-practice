from start import helper
helper()  # Assuming this is some custom function you want to call.

import sqlite3

# Connect to the SQLite database (titanic.db)
connection = sqlite3.connect("titanic.db")
cursor = connection.cursor()

# Create table named new_table if it does not exist already
cursor.execute("""
CREATE TABLE IF NOT EXISTS new_table (
  name TEXT,
  age INTEGER,
  username TEXT,
  pay_rate REAL
)
""")

# Insert single row of values into new_table
cursor.execute("""
    INSERT INTO new_table (
        name,
        age,
        username,
        pay_rate
    )
    VALUES (?, ?, ?, ?)
""", ("Bob Peterson", 34, "bob1234", 40.00))

# Here is the new_rows object
new_rows = [('Anne Smith', 33, 'AS896', 25.00),
            ('Billy Roberts', 29, 'bill5Rob', 30.00),
            ('Jason Johnson', 48, 'JasonJ77', 40.00),
            ('Tim Trunk', 51, 'Timtrunk4', 40.00),
            ('Sarah Fall',19, 'SFall232', 25.00)
            ]

# Insert new_rows into the new_table table
cursor.executemany("""INSERT INTO new_table VALUES (?,?,?,?)""", new_rows)

# Commit the transaction to save changes
connection.commit()

# Fetch all rows from the table
cursor.execute("SELECT * FROM new_table")
rows = cursor.fetchall()

# Print the rows
for row in rows:
    print(f"Name: {row[0]}, Age: {row[1]}, Username: {row[2]}, Pay Rate: {row[3]}")

# Close the connection
connection.close()
