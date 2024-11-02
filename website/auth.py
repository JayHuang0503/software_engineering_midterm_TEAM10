from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_user, login_required, logout_user
from .models import Students
from . import db

auth = Blueprint("auth", __name__)

# @auth.route("/student-sign-up", methods=["GET", "POST"])
# def sign_up():
#     name = ""
#     if request.method == "POST":
#         name = request.form.get("name")
#         email = request.form.get("email")
#         password1 = request.form.get("password1")
#         print(password1)
#         password2 = request.form.get("password2")
#         role_type = request.form.get("role_type")
#         role_id = ord(role_type) - ord("0")
#         verification = request.form.get("verification")

#         if Teacher.query.filter_by(email=email).first():
#             flash("Email is already in use.", category="error")
#         elif len(password1) < 6:
#             flash("Password should be at least 6 characters.", category="error")
#         elif password1 != password2:
#             flash("Passwords don\'t match.", category="error")
#         # elif role_id == 0:
#         #     flash("Please choose a role.", category="error")
#         elif verification != "chuchuchu":
#             flash("Wrong verification", category="error")
#         else:
#             role = Role.query.filter_by(role_id=role_id).first()
#             teacher = Teacher(email, name, generate_password_hash(password1), role_id)
#             role.teachers.append(teacher)
#             db.session.add(teacher)
#             db.session.commit()

#             login_user(teacher, remember=True)
#             flash("Teacher created.", category="success")
#             return redirect(url_for("views.home"))

#     return render_template("signup.html", user=current_user, last_name=name, last_email=email)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.login_page"))


@auth.route("/login", methods=["GET", "POST"])
def login():
    student_id = ""
    if request.method == "POST":
        student_id = request.form.get("student_id")

        student = Students.query.filter_by(student_id=student_id).first()

        if student != None:
            flash("Logged in.", category="success")
            login_user(student, remember=True)
            return redirect(url_for("views.you_logged_in"))
        else:
            flash(f"Student [{student_id}] does not exist.", category="error")

    return render_template("login.html", user=current_user)
