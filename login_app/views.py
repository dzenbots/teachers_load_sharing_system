from login_app import login_app, check_user_valid, login_user
from flask import redirect, url_for, request, session


@login_app.route("/")
@login_app.route("/login")
@check_user_valid
def login():
    return redirect(url_for('index'))


@login_app.route("/on_login", methods=['POST'])
def on_login():
    if not login_user(request.form.get('login'), request.form.get('password')):
        session['login_message'] = "Неверный логин или пароль"
    return redirect(url_for('login_app.login'))


@login_app.route("/logout")
@check_user_valid
def logout():
    session.pop('valid_user')
    session.pop('login')
    return redirect(url_for('index'))
