from flask import Blueprint, render_template, request, session, redirect, url_for
from . import login_user, check_user_valid


login_app = Blueprint("login_app", __name__, static_folder="static", template_folder="templates", url_prefix="/login_app")


@login_app.route("/")
@login_app.route("/login")
def login():
    if check_user_valid():
        return redirect(url_for('main.index'))
    else:
        return render_template("login_app.html",
                               message=session.pop('login_message') if 'login_message' in session else None)


@login_app.route("/login", methods=['POST'])
def on_login():
    if login_user(request.form.get('login'), request.form.get('password')):
        return redirect(url_for('main.index'))
    else:
        session['login_message'] = "Неверный логин или пароль"
        return redirect(url_for('login_app.login'))


@login_app.route("/logout")
def logout():
    if 'valid_user' in session:
        session.pop('valid_user')
    if 'login' in session:
        session.pop('login')
    return redirect(url_for('index'))
