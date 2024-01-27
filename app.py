from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User 
import os

app = Flask(__name__)

# TODO: Replace these hard-coded variables for security
os.environ['DB_USERNAME'] = 'N'
os.environ['DB_PASSWORD'] = ' '
os.environ['DB_NAME'] = 'users'

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.environ['DB_USERNAME']}:{os.environ['DB_PASSWORD']}@localhost/{os.environ['DB_NAME']}"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.config['SQLALCHEMY_ECHO'] = True
app.config ['SECRET_KEY'] = 'abc123'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False 

debug = DebugToolbarExtension(app)


connect_db(app)

@app.route('/')
def home():
    return redirect("/users")

@app.route('/users')
def show_users():
    users = User.query.all()
    return render_template('home.html', users=users)

@app.route ('/users/new')
def get_new_user_form():
    return render_template('new-user.html')

@app.route ('/users/new', methods=['POST'])
def create_user():
    new_first = request.form['first_name']
    new_last = request.form['last_name']
    new_image = request.form['image_url']

    new_user = User(first_name=new_first,last_name=new_last,image_url=new_image)
    db.session.add(new_user)
    db.session.commit()

    return redirect("/")

@app.route ('/users/<user_id>')
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("user.html", user=user)

@app.route ('/users/<user_id>/edit')
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('edit-user.html', user=user)

@app.route('/users/<user_id>/edit', methods=['POST'])
def update_user(user_id):
    existing_user = User.query.get(user_id)

    if not existing_user:
        flash('User does not exist')
        return redirect('/')  # Redirect to an error page or handle appropriately

    new_first = request.form['newFirst']
    new_last = request.form['newLast']
    new_image = request.form['newImg']

    # Update the existing user's properties
    existing_user.first_name = new_first
    existing_user.last_name = new_last
    existing_user.image_url = new_image

    db.session.commit()

    return redirect(f"/users/{user_id}")

@app.route ('/users/<user_id>/delete', methods=['POST'])
def delete_user(user_id):
    User.query.filter_by(id=user_id).delete()
    db.session.commit()
    flash('User deleted.')
    return redirect('/')

