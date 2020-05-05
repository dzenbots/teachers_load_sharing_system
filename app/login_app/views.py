from flask import Blueprint, render_template, request, session, redirect, url_for
from app.login_app import check_user_valid, login_user

login_app = Blueprint("login_app",
                      __name__,
                      static_folder="static",
                      template_folder="templates",
                      url_prefix="/login_app")


@login_app.route("/")
@login_app.route("/login")
@check_user_valid
def login():
    return redirect(url_for('main.index'))


@login_app.route("/login", methods=['POST'])
def on_login():
    if login_user(request.form.get('login'), request.form.get('password')):
        return redirect(url_for('main.index'))
    else:
        session['login_message'] = "Неверный логин или пароль"
        return redirect(url_for('login_app.login'))


@login_app.route("/logout")
@check_user_valid
def logout():
    session.pop('valid_user')
    session.pop('login')
    return redirect(url_for('main.index'))
