from flask import render_template

from index import app
from login_app import check_user_valid


@app.errorhandler(404)
def http_404_handler(error):
    return render_template('404_error.html')


@app.route("/")
@app.route("/index")
@check_user_valid
def index():
    return render_template('index.html')
