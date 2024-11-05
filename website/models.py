from flask_login import UserMixin
from . import db
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy

class Students(db.Model, UserMixin):
    __tablename__ = "students"

    def __init__(self, student_id, name):
        self.student_id = student_id
        self.name = name

    def get_id(self):
        return (self.student_id)

    student_id = db.Column(db.String(6), primary_key=True)
    name = db.Column(db.String(50))
    # password = db.Column(db.String(150))
    # self_introduction = db.Column(db.String(500), nullable=True)
    # photo = db.Column(db.String(150), nullable=True)
    # offict_phone = db.Column(db.String(10), nullable=True)
    # personal_website = db.Column(db.String(150), nullable=True)
    # interest = db.Column(db.String(150), nullable=True)
    # school = db.Column(db.String(150), nullable=True)

    # role_id = db.Column(db.ForeignKey("roles.role_id"))

    def __repr__(self):
        return f"stuent id: {self.student_id}, name: {self.name}"

class Courses(db.Model):
    __tablename__ = "courses"

    def __init__(self, course_id, course_name, teacher_name, weekday, course_time, lang, course_for) -> None:
        self.course_id = course_id
        self.course_name = course_name
        self.teacher_name = teacher_name
        self.weekday = weekday
        self.course_time = course_time
        self.lang = lang
        self.course_for = course_for

    def get_id(self):
        return self.course_id

    course_id = db.Column(db.String(4), primary_key=True)
    course_name = db.Column(db.String(50))
    teacher_name = db.Column(db.String(50))
    weekday = db.Column(db.String(50))
    course_time = db.Column(db.String(50))
    lang = db.Column(db.String(50))
    course_for = db.Column(db.String(50))

    def __repr__(self):
        return f"course id: {self.course_id}, course name: {self.course_name}, teacher name: {self.teacher_name}, weekday: {self.weekday}, course time: {self.course_time}, language: {self.lang}, course for: {self.course_for}"

    def to_dict(self):
        return {field.name:getattr(self, field.name) for field in self.__table__.c}
