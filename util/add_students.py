import sqlite3

con = sqlite3.connect("instance/database.db")
cur = con.cursor()

# (student_id, name)
predefine_students = [
    ("D00001", "Harry Potter"),
    ("D00002", "YuYou"),
]

cur.executemany("INSERT INTO students VALUES(?, ?)", predefine_students)
con.commit()