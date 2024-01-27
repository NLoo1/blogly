from datetime import datetime
from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import Post, db, connect_db, User 
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
    posts = Post.query.filter_by(created_by=user_id).all()
    return render_template("user.html", user=user, posts=posts)

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
    Post.query.filter_by(created_by=user_id).delete()
    User.query.filter_by(id=user_id).delete()
    db.session.commit()
    flash('User deleted.')
    return redirect('/')

@app.route('/users/<user_id>/posts/new')
def show_post_form(user_id):
    user = User.query.get(user_id)
    return render_template('new-post.html',user=user)


@app.route('/users/<user_id>/posts/new', methods=['POST'])
def add_post(user_id):
    title = request.form['title']
    content = request.form['content']
    time = datetime.now()
    new_post = Post(title=title,content=content,created_at=time,created_by=user_id)
    db.session.add(new_post)
    db.session.commit()
    return redirect(f"/users/{user_id}")

@app.route('/posts/<post_id>')
def get_post(post_id):
    post = Post.query.get(post_id)
    author = db.session.query(User).filter(User.id == post.created_by).all()
    return render_template('post.html', post=post, author=author)

@app.route('/posts/<post_id>/edit')
def edit_form_for_post(post_id):
    post = Post.query.get(post_id)
    return render_template('edit-post.html', post=post)

@app.route('/posts/<post_id>/edit', methods=['POST'])
def edit_post(post_id):
    existing_post = Post.query.get(post_id)

    if not existing_post:
        flash('Post does not exist')
        return redirect('/')  # Redirect to an error page or handle appropriately

    title = request.form['newTitle']
    content = request.form['newContent']

    # Update the existing user's properties
    existing_post.title = title
    existing_post.content = content

    db.session.commit()

    return redirect(f'/posts/{post_id}')

@app.route('/posts/<post_id>/delete', methods=['POST'])
def delete_post(post_id):
    Post.query.filter_by(id=post_id).delete()
    db.session.commit()
    flash('Post deleted.')
    return redirect('/')
