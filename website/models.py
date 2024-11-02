from flask_login import UserMixin
from . import db
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy#SQLAlchemyclass

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
