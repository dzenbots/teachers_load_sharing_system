from flask import Flask, render_template, g

from app.classes_app.views import classes_app
from app.login_app.views import login_app
from app.subjects_app.views import subjects_app
from app.views import main

# from app.models import db


def create_app(config_file='settings.py'):
    app = Flask(__name__)
    app.config.from_pyfile(config_file)
    g.database = app.config.get('DB_FILE_PATH').get('DB_FILE_PATH')

    # db.init(database=g.get('database').get('DB_FILE_PATH'))
    app.register_blueprint(main)
    app.register_blueprint(login_app)
    app.register_blueprint(subjects_app)
    app.register_blueprint(classes_app)

    @app.errorhandler(404)
    def http_404_handler(error):
        return render_template('404_error.html')

    return app
