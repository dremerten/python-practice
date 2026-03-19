"""
 The following code will iterate through each row in the students table 
 and print each row where the Grade field is 'Pass'.
"""
import sqlite3

connection = sqlite3.connect("titanic.db")
cursor = connection.cursor()

for row in cursor.execute('''SELECT * FROM students WHERE Grade = 'Pass';'''):
   print(row)

# save all rows from a field with .fetchall() then use a for loop to find some sort of result.`
major_codes = cursor.execute("SELECT major_code FROM students;").fetchall()
 
 
# Obtain the average of the tuple list by using for loops
sum = 0
for num in major_codes: 
  sum = sum + num[0]
average = sum / len(major_codes)
 
# Show average
print(average)