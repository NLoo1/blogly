from models import db, connect_db 
from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.config['SQLALCHEMY_ECHO'] = True
app.config ['SECRET_KEY'] = 'abc123'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False 

debug = DebugToolbarExtension(app)


connect_db(app)

@app.route('/')
def home():
    return ''

@app.route('/users')
def show_users():
    return ''

@app.route ('/users/new')
def get_new_user_form():
    return ''

@app.route ('/users/new', methods=['POST'])
def create_user():
    return ''

@app.route ('/users/<user_id>')
def get_user(user_id):
    return ''

@app.route ('/users/<user_id>/edit')
def edit_user(user_id):
    return ''


@app.route ('/users/<user_id>/edit', methods=['POST'])
def update_user(user_id):
    return ''
