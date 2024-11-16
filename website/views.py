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

        course_name = request.form.get("course_name") or None

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
        if course_name != None:
            filters.append(Courses.course_name.like('%'+course_name+'%'))
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
        target = []
        # Has some criterias
        if filters:
            target = Courses.query.filter(and_(*filters)).all()
            if len(target) == 0:
                target = None
        # Empty criteria, then show all courses
        else:
            target = Courses.query.all()

        if target != None:
            for i in range(len(target)):
                target[i] = target[i].__dict__
        return render_template("search.html", user=current_user, target_courses=target)
    else:
        return render_template("search.html", user=current_user, first_time=True)

@views.route('/course/<course_id>', methods=["GET", "POST"])
def course_content(course_id):
    if request.method == "POST":
        pass
    else:
        target_course = Courses.query.filter_by(course_id=course_id).first()
        # Turn into dict
        target_course = target_course.__dict__
        # Make weekday to chinese
        new_weekday = ""
        for day in target_course["weekday"]:
            if day == "1": new_weekday += "一"
            elif day == "2": new_weekday += "二"
            elif day == "3": new_weekday += "三"
            elif day == "4": new_weekday += "四"
            elif day == "5": new_weekday += "五"
            elif day == "6": new_weekday += "六"
            elif day == "7": new_weekday += "日"
            elif day == ";": new_weekday += "、"
        target_course["weekday"] = new_weekday
        # Make course time better to view
        new_course_time = ""
        for t in target_course["course_time"]:
            if t == ";": new_course_time += "、"
            else: new_course_time += t
        target_course["course_time"] = new_course_time
        print(target_course)
        return render_template("course_content.html", user=current_user, target_course=target_course)