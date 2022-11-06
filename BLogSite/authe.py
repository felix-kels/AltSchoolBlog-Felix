from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
# from flask_mail import Mail, Message
# from config import mail_username, mail_password


authe = Blueprint("authe", __name__)
# mail = Mail(authe)


@authe.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in!", category="success")
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("Incorrect Password", category="error")
        else:
            flash("Email does not exist", category="error")

    return render_template("login.html", user=current_user)


@authe.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        email_exits = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()

        if email_exits:
            flash("Email already exists.", category="error")
        elif username_exists:
            flash("Username already exists.", category="error")
        elif password1 != password2:
            flash("Password don't match", category="error")
        elif len(username) < 3:
            flash("Username is too short", category="error")
        elif len(password1) < 5:
            flash("Password is too short", category="error")
        elif len(email) < 3:
            flash("Invalid Email", category="error")
        else:
            new_user = User(email=email, username=username, first_name=first_name, last_name=last_name, password=generate_password_hash(password2, method="sha256"))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("User Created Successfully!")
            return redirect(url_for("views.home"))

    return render_template("sign_up.html", user=current_user)


@authe.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.home"))


@authe.route("/about", methods=["GET", "POST"])
def about():
    return render_template("about.html", user=current_user)


@authe.route("/contact-me", methods=["GET", "POST"])
def contact():
    # if request.method == "POST":
    #     name = request.form.get('name')
    #     email = request.form.get('email')
    #     message = request.form.get('message')
    #
    #     msg = Message(subject=f'New mail from {name}', body=f'Name: {name}\nE-mail: {email}\n{message}',
    #                   sender=mail_username, recipients=['kelechifelix9065@gmail.com'])
    #     mail.send(msg)
        flash('Sent!')

        return render_template("contact.html", user=current_user, success=True)







