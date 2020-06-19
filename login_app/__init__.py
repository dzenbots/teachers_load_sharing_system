from functools import wraps

from flask import Blueprint, session, render_template

login_app = Blueprint('login_app',
                      __name__,
                      static_folder='static',
                      template_folder='templates',
                      url_prefix='/login_app')

admin_users = [
    dict(
        login='admin', password="@dm!n"
    )
]

reg_users = [
    dict(
        login='user', password='1'
    )
]

valid_users = dict(admin_users=admin_users)


def login_user(user_login, password):
    for item in valid_users:
        for user in valid_users.get(item):
            if (user.get("login") == user_login) and (user.get("password") == password):
                session['valid_user'] = True
                session['login'] = user_login
                return True
    return False


def check_user_valid(original_function):
    @wraps(original_function)
    def wrapper(*args, **kwargs):
        if 'valid_user' in session:
            return original_function(*args, **kwargs)
        else:
            return render_template("login_app.html",
                                   message=session.pop('login_message') if 'login_message' in session else None)

    return wrapper


from login_app import views
