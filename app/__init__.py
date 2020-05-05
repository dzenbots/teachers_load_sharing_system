from flask import Flask, render_template
from .views import main


def create_app(config_file='settings.py'):

    app = Flask(__name__)
    app.config.from_pyfile(config_file)
    app.register_blueprint(main)

    @app.errorhandler(404)
    def http_404_handler(error):
        return render_template('404_error.html')

    return app
