# project/__init__.py


import os

from flask import Flask, jsonify
from flask_cors import CORS


def create_app():

    # instantiate the app
    app = Flask(__name__)

    # enable CORS
    CORS(app)

    # set config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    # register blueprints
    from project.api.eval import eval_blueprint
    app.register_blueprint(eval_blueprint)

    return app
