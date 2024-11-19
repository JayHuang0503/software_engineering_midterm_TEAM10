from flask import Blueprint, request, flash, redirect, url_for, render_template, jsonify
from flask_login import current_user, login_required
from sqlalchemy import or_, and_
from . import db
from .models import Courses, Selections
from collections import defaultdict

views = Blueprint("views", __name__)

FILTER = []
# filter the courses
def fileter_targets():
    global FILTER
    filters = FILTER
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
    return target

# Get the courses data to decide to show add/follow button or not
def lebel_targets(target):
    if not target: return None
    # Get the courses that this student has added
    added_courses = [s.course_id for s in Selections.query.filter_by(student_id=current_user.student_id, class_state="加選").all()]
    followed_courses = [s.course_id for s in Selections.query.filter_by(student_id=current_user.student_id, class_state="關注").all()]
    # print("added:", added_courses)
    for i in range(len(target)):
        target[i] = target[i].__dict__
        if target[i]["course_id"] in added_courses:
            target[i]["show_add_button"] = False
            target[i]["follow_button_state"] = "disable"
        else:
            target[i]["show_add_button"] = True
            if target[i]["course_id"] in followed_courses:
                target[i]["follow_button_state"] = "unfollow"
            else:
                target[i]["follow_button_state"] = "follow"
    return target


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
        global FILTER
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

        FILTER = filters

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
            target = lebel_targets(target)
        return render_template("search.html", user=current_user, target_courses=target)
    else:
        target = lebel_targets(fileter_targets())
        return render_template("search.html", user=current_user, target_courses=target)

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

@login_required
@views.route('/withdraw/<course_id>', methods=["GET", "POST"])
def withdraw(course_id):
    course = Courses.query.filter_by(course_id=course_id).first()

    if request.method == "GET":
        if current_user.getTotalCredits() - course.credit < 12: # 學分數不得低於12學分
            flash("學分數不得低於12學分", "error")
            return redirect(url_for("views.personal_schedule"))
        return render_template("withdrawConfirm.html", user=current_user, course=course)

    elif request.method == "POST":
        course.remaining_quota += 1
        Selections.query.filter_by(student_id=current_user.student_id, course_id=course_id).delete()
        db.session.commit()
        flash("退選成功")
        return redirect(url_for("views.personal_schedule")) 

@login_required
@views.route('/schedule')
def personal_schedule():
    # 準備課表數據結構
    schedule = defaultdict(list)
    total_credits = 0
    counted_courses = set()  # 用來避免同一堂課重複累加學分

    # 獲取當前學生的已加選課程和關注清單
    added_courses = {s.course_id: s for s in Selections.query.filter_by(student_id=current_user.student_id, class_state="加選").all()}
    followed_courses = {s.course_id: s for s in Selections.query.filter_by(student_id=current_user.student_id, class_state="關注").all()}

    # 分析所有相關課程
    for course in Courses.query.all():
        weekdays = course.weekday.split(";")
        periods_list = course.course_time.split(";")
        for weekday, periods in zip(weekdays, periods_list):
            for period in map(int, periods.split(",")):
                is_added = course.course_id in added_courses
                is_followed = course.course_id in followed_courses
                is_conflict = False
                if course.course_type == "必修" and course.course_for == current_user.major:
                    is_necessary = True
                else:
                    is_necessary = False

                # 判斷是否衝堂
                if is_added or is_followed:
                    for other in schedule.get((int(weekday), period), []):
                        if other["is_added"] or other["is_followed"]:
                            is_conflict = True
                            other["is_conflict"] = True

                # 累積學分
                if is_added and course.course_id not in counted_courses:
                    total_credits += course.credit
                    counted_courses.add(course.course_id)  # 確保學分只累加一次

                # 添加課程到課表
                schedule[(int(weekday), period)].append({
                    "course_id": course.course_id,
                    "course_name": course.course_name,
                    "teacher_name": course.teacher_name,
                    "credit": course.credit,
                    "is_added": is_added,
                    "is_followed": is_followed,
                    "is_conflict": is_conflict,
                    "is_necessary": is_necessary
                })

    return render_template("schedule.html", user=current_user, schedule=schedule, total_credits=total_credits)

from collections import defaultdict

@login_required
@views.route('/add/<course_id>', methods=["GET", "POST"])
def add_selection(course_id):
    # 查詢課程資料
    course = Courses.query.filter_by(course_id=course_id).first()
    if not course:
        flash("課程不存在", category="error")
        return redirect(url_for("views.search"))

    # 解析欲加選課程的時間
    course_weekday = course.weekday  # 課程的星期幾
    course_time = course.course_time  # 課程的時間段，例如 "08:00-10:00"

    # 檢查學分是否超出限制
    if current_user.getTotalCredits() + course.credit > 25:
        flash("學分數不得高於25學分", category="error")
        return redirect(url_for("views.search"))

    # 查詢學生已加選課程
    added_courses = Selections.query.filter_by(student_id=current_user.student_id, class_state="加選").all()

    # 建立學生已選課程的時間表
    schedule = defaultdict(list)
    for selected in added_courses:
        selected_course = Courses.query.filter_by(course_id=selected.course_id).first()
        if selected_course:
            schedule[selected_course.weekday].append(selected_course.course_time)

    # 檢查是否與已選課程時間衝突
    if course_time in schedule[course_weekday]:
        flash("加選失敗，課程時間與已選課程衝突")
        return redirect(url_for("views.search"))

    # 查詢學生選課記錄
    existing_selection = Selections.query.filter_by(
        student_id=current_user.student_id,
        course_id=course_id
    ).first()

    # 已存在選課記錄的情況處理
    if existing_selection:
        if existing_selection.class_state == "加選":
            flash("加選失敗，課程已加選", category="error")
            return redirect(url_for("views.search"))
        elif existing_selection.class_state == "關注":
            # 更新關注狀態為加選
            existing_selection.class_state = "加選"
            if course.remaining_quota >= 1:
                course.remaining_quota -= 1
                db.session.commit()
                flash("課程已成功從關注狀態更新為加選", category="info")
                return redirect(url_for("views.search"))
            else:
                flash("課程餘額不足", category="error")
                return redirect(url_for("views.search"))

    # 處理加選邏輯（沒有選課記錄的情況）
    if course.remaining_quota >= 1:
        new_selection = Selections(
            student_id=current_user.student_id,
            course_id=course_id,
            class_state="加選"
        )
        db.session.add(new_selection)
        course.remaining_quota -= 1
        db.session.commit()
        flash("加選成功")
        return redirect(url_for("views.search"))
    else:
        flash("課程餘額不足", category="error")
        return redirect(url_for("views.search"))

@login_required
@views.route('/follow/<course_id>', methods=["GET", "POST"])
def add_follow(course_id):
    """
    - 如果課程已加選或已關注，阻止再次關注。
    """
    # 查詢是否已存在選課紀錄
    existing_selection = Selections.query.filter_by(
        student_id=current_user.student_id,
        course_id=course_id
    ).first()

    # 若課程已加選或已關注，阻止操作
    if existing_selection:
        if existing_selection.class_state == "加選":
            flash("課程已加選，無法再次關注", category="error")
            return redirect(url_for("views.search"))
        elif existing_selection.class_state == "關注":
            # flash("課程已關注，無法重複關注")
            flash("已取消關注此課程", category="info")
            db.session.delete(existing_selection)
            db.session.commit()
            return redirect(url_for("views.search"))

    # 新增關注記錄
    new_selection = Selections(
        student_id=current_user.student_id,
        course_id=course_id,
        class_state="關注"
    )
    db.session.add(new_selection)
    db.session.commit()

    flash("課程關注成功")
    return redirect(url_for("views.search"))