import sqlite3

# (student_id, name, major)
predefine_students = [
    ("D00001", "Student 1", "資訊一甲"),
    ("D00002", "Student 2", "資訊二甲"),
    ("D00003", "Student 3", "資訊二甲"),
    ("D00004", "Student 4", "會計二甲"),
    ("D00005", "Student 5", "外文一甲"),
]


if __name__ == "__main__":
    con = sqlite3.connect("instance/database.db")
    cur = con.cursor()
    cur.executemany("INSERT INTO students VALUES(?, ?, ?)", predefine_students)
    con.commit()