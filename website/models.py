from flask_login import UserMixin
from . import db
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy

class Students(db.Model, UserMixin):
    '''
    Attributes:
        student_id : 學號
        name       : 學生姓名
    '''
    __tablename__ = "students"

    def __init__(self, student_id, name):
        self.student_id = student_id
        self.name = name

    def get_id(self):
        return (self.student_id)

    student_id = db.Column(db.String(6), primary_key=True)
    name = db.Column(db.String(50))

    def __repr__(self):
        return f"stuent id: {self.student_id}, name: {self.name}"

class Courses(db.Model):
    '''
    Attributes:
        course_id    : 課程代碼, string
        course_name  : 課程名稱, string
        teacher_name : 教師姓名, string
        credit       : 學分數, integer
        course_type  : 課程類別 (必修/選修), string
        weekday      : 星期, string
        course_time  : 節次, string
        lang         : 授課語言, string
        course_for   : 開課班級, string
    '''
    __tablename__ = "courses"

    def __init__(self, course_id, course_name, teacher_name, credit, course_type, weekday, course_time, lang, course_for) -> None:
        self.course_id = course_id
        self.course_name = course_name
        self.teacher_name = teacher_name
        self.credit = credit
        self.course_type = course_type
        self.weekday = weekday
        self.course_time = course_time
        self.lang = lang
        self.course_for = course_for

    def get_id(self):
        return self.course_id

    course_id = db.Column(db.String(4), primary_key=True)
    course_name = db.Column(db.String(50))
    teacher_name = db.Column(db.String(50))
    credit = db.Column(db.Integer)
    course_type = db.Column(db.String(2))
    weekday = db.Column(db.String(50))
    course_time = db.Column(db.String(50))
    lang = db.Column(db.String(50))
    course_for = db.Column(db.String(50))

    def __repr__(self):
        return f"course id: {self.course_id}, course name: {self.course_name}, teacher name: {self.teacher_name}, credit: {self.credit}, course type: {self.course_type}, weekday: {self.weekday}, course time: {self.course_time}, language: {self.lang}, course for: {self.course_for}"

    def to_dict(self):
        return {field.name:getattr(self, field.name) for field in self.__table__.c}
