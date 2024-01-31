# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
import os

db = SQLAlchemy()
toolbar = DebugToolbarExtension()

def create_app(config_class='config.Config'):
    app = Flask(__name__)
    app.config ['SECRET_KEY'] = 'abc123'
    app.config.from_object(config_class)

    db.init_app(app)

    # Import and register blueprints, if any

    return app
