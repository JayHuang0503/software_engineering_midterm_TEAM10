import sqlite3

con = sqlite3.connect("instance/database.db")
cur = con.cursor()

# (student_id, name)
predefine_students = [
    ("D00001", "Student 1"),
    ("D00002", "Student 2"),
    ("D00003", "Student 3"),
]

cur.executemany("INSERT INTO students VALUES(?, ?)", predefine_students)
con.commit()