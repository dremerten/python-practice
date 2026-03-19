def helper():
  import sqlite3
  connection = sqlite3.connect("titanic.db")
  cursor = connection.cursor()
  cursor.execute('''DROP TABLE IF EXISTS new_table''')