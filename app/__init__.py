from flask import Flask, render_template, session
from .views import main
from .login_app.views import login_app


def create_app(config_file='settings.py'):

    app = Flask(__name__)
    app.config.from_pyfile(config_file)
    app.register_blueprint(main)
    app.register_blueprint(login_app)

    @app.errorhandler(404)
    def http_404_handler(error):
        return render_template('404_error.html')

    return app
