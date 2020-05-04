from flask import Flask
from config import config
from extensions import db, login_manager
import os


def creat_app(config_name=None):
    if not config_name:
        config_name = os.getenv('FLASK_CONFIG', 'default')
    app = Flask(__name__)

    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    login_manager.init_app(app)
    db.init_app(app)

    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
