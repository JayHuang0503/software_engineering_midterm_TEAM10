from flask import Blueprint, request, flash, redirect, url_for, render_template, jsonify
from flask_login import current_user, login_required
from sqlalchemy import or_, and_
from . import db
from .models import Courses

views = Blueprint("views", __name__)


# domain root
@views.route('/')
@views.route('/home')
def home():
    return render_template("home.html", user=current_user)


# @login_required
@views.route('/search', methods=["GET", "POST"])
def search():
    if request.method == "POST":
        # Get search criteria
        course_id = request.form.get("course_id") or None

        teacher_name = request.form.get("teacher_name") or None

        weekday = request.form.get("weekday")
        if weekday == '0': weekday = None

        course_time = request.form.get("course_time")
        if course_time == '0': course_time = None

        lang = request.form.get("lang")
        if lang == "0": lang = None

        course_for = request.form.get("course_for") or None

        print(f"course id: {course_id},\nteacher name: {teacher_name},\nweekday: {weekday},\ncourse time: {course_time},\nlang: {lang},\ncourse for: {course_for}")

        # Create filter
        filters = []
        if course_id != None:
            filters.append(Courses.course_id == course_id)
        if teacher_name != None:
            filters.append(Courses.teacher_name.like('%'+teacher_name+'%'))
        if weekday != None:
            filters.append(Courses.weekday.like('%'+weekday+'%'))
        if course_time != None:
            # It has bug here
            filters.append(Courses.course_time.like('%'+course_time+'%'))
        if lang != None:
            filters.append(Courses.lang == lang)
        if course_for != None:
            filters.append(Courses.course_for.like('%'+course_for+'%'))

        # Query
        target_courses = []
        # Has some criterias
        if filters:
            target_courses = Courses.query.filter(and_(*filters)).all()
        # Empty criteria, then show all courses
        else:
            target_courses = Courses.query.all()

        for target_course in target_courses:
            print(target_course)
        return render_template("search.html", user=current_user, target_courses=target_courses)
    else:
        return render_template("search.html", user=current_user)
