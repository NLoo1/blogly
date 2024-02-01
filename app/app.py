# import sys 
# sys.path.append('C:\\Users\\NLoo1\\Desktop\\repos\\blogly')

import os
from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db
from user_routes import user_bp
from post_routes import post_bp

app = Flask(__name__)

# TODO: Replace these hard-coded variables for security
os.environ['DB_USERNAME'] = 'NLoo1'
os.environ['DB_PASSWORD'] = ' '
os.environ['DB_NAME'] = 'users'

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.environ['DB_USERNAME']}:{os.environ['DB_PASSWORD']}@localhost/{os.environ['DB_NAME']}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'abc123'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)

app.register_blueprint(user_bp)
app.register_blueprint(post_bp)

if __name__ == '__main__':
    app.run(debug=True)
