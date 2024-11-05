import sqlite3

con = sqlite3.connect("instance/database.db")
cur = con.cursor()

# (course_id, teacher_name, weekday, course_time, lang, class_for)
# weekday用數字加分號的方式, 例如: "1;3", 代表星期一跟星期三
# course_time用逗號與分號的方式, 例如: "2,3,4;7,8", 代表第2,3,4節 跟 7,8節
# 綜合以上的weekday跟course_time, 意思為: 星期一的2,3,4節 跟 星期三的7,8節
# 註: 不要有空格
predefine_courses = [
    ("0001", "Teacher 1", "1;3", "2,3,4;7,8", "中文", "資訊一甲"),
    ("0002", "Teacher 2", "2;4;5", "1;6,7,8;3,4", "英文", "外文一甲")
]

cur.executemany("INSERT INTO courses VALUES(?, ?, ?, ?, ?, ?)", predefine_courses)
con.commit()