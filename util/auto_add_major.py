import sqlite3
from add_students import predefine_students
from add_courses import predefine_courses


if __name__ == "__main__":
    con = sqlite3.connect("instance/database.db")
    cur = con.cursor()

    major_courses = []
    for student in predefine_students:
        for course in predefine_courses:
            if student[2] == course[10]:
                if course[6] > 0:
                    con.execute("UPDATE courses set remaining_quota=remaining_quota-? where course_id = ?", (1, course[0])) 
                    con.commit()
                    major_courses.append((student[0], course[0], "加選"))


    cur.executemany("INSERT INTO selections VALUES(?, ?, ?)", major_courses)
    con.commit()