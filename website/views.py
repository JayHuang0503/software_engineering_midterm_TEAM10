from flask import Blueprint, request, flash, redirect, url_for, render_template, jsonify
from flask_login import current_user, login_required
from . import db

views = Blueprint("views", __name__)


# domain root
@views.route('/')
@views.route('/home')
def login_page():
    return redirect(url_for("auth.login"))
    # return 'Hello, World!'

# @login_required
@views.route('/logged-in')
def you_logged_in():
    return render_template("logged-in.html", user=current_user)

# @views.route('/add-user', methods=['GET', 'POST'])
# def addUser():
#     if request.method == "POST":
#         phone = request.form.get("phone")
#         name = request.form.get("name")
#         new_user = User(phone, name)
#         db.session.add(new_user)
#         db.session.commit()
#         return jsonify(new_user.to_dict())
#     else:
#         return render_template("add_user.html")