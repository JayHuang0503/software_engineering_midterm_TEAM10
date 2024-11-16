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

    selections = db.relationship('Selections', backref='student', lazy=True)
    
    def getTotalCredits(self): # 取得學生學分數
        totalCredits = 0
        for selection in self.selections:
            course = Courses.query.get(selection.course_id)
            if course:
                totalCredits += course.credit
        return totalCredits

    def __repr__(self):
        return f"stuent id: {self.student_id}, name: {self.name}"

class Courses(db.Model):
    '''
    Attributes:
        course_id       : 課程代碼, string
        course_name     : 課程名稱, string
        teacher_name    : 教師姓名, string
        credit          : 學分數, integer
        course_type     : 課程類別 (必修/選修), string
        course_quota    : 開課名額
        remaining_quota : 剩餘名額
        weekday         : 星期, string
        course_time     : 節次, string
        lang            : 授課語言, string
        course_for      : 開課班級, string
    '''
    __tablename__ = "courses"

    def __init__(self, course_id, course_name, teacher_name, credit, course_type, course_quota, remaining_quota, weekday, course_time, lang, course_for) -> None:
        self.course_id = course_id
        self.course_name = course_name
        self.teacher_name = teacher_name
        self.credit = credit
        self.course_type = course_type
        self.course_quota = course_quota
        self.remaining_quota = remaining_quota
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
    course_quota = db.Column(db.Integer)
    remaining_quota = db.Column(db.Integer)
    weekday = db.Column(db.String(50))
    course_time = db.Column(db.String(50))
    lang = db.Column(db.String(50))
    course_for = db.Column(db.String(50))

    # class_state = db.Column(db.String(50))

    def __repr__(self):
        return f"course id: {self.course_id}, course name: {self.course_name}, teacher name: {self.teacher_name}, credit: {self.credit}, course type: {self.course_type}, course quota: {self.course_quota}, remaining quota: {self.remaining_quota}, weekday: {self.weekday}, course time: {self.course_time}, language: {self.lang}, course for: {self.course_for}"

    def to_dict(self):
        return {field.name:getattr(self, field.name) for field in self.__table__.c}

class Selections(db.Model): # 學生選上的課程
    '''
    Attributes:
        student_id : 學號, string
        course_id  : 課程代碼, string
        class_state: 課程狀態 已加選/關注, string
    '''
    __tablename__ = "selections"

    def __init__(self, student_id, course_id):
        self.student_id = student_id
        self.course_id = course_id
        # self.class_state = class_state
    
    student_id = db.Column(db.String(6), db.ForeignKey("students.student_id"), primary_key=True)
    course_id = db.Column(db.String(4), db.ForeignKey("courses.course_id"), primary_key=True)

    def __repr__(self):
        return f"student id: {self.student_id}, course id: {self.course_id}"