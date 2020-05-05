from flask import session


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


def check_user_valid():
    if 'valid_user' in session:
        return session.get('valid_user')
    return False
