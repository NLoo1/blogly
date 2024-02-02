# app/__init__.py

import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
from .models import db
from .user_routes import user_bp
from .post_routes import post_bp

debug = DebugToolbarExtension()

def create_app(config_class='config.Config'):

    load_dotenv()

    app = Flask(__name__)
    app.config ['SECRET_KEY'] = 'abc123'
    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.environ.get('DB_USERNAME')}: @localhost/{os.environ.get('DB_NAME')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SECRET_KEY'] = 'abc123'
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

    db.init_app(app)
    # Import and register blueprints, if any
    app.register_blueprint(user_bp)
    app.register_blueprint(post_bp)

    return app
