from flask import Blueprint, flash, redirect, render_template, request
from models import User, Post, db


user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/')
def home():
    return redirect("/users")

@user_bp.route('/users')
def show_users():
    users = User.query.all()
    return render_template('home.html', users=users)

@user_bp.route ('/users/new')
def get_new_user_form():
    return render_template('new-user.html')

@user_bp.route ('/users/<user_id>')
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(created_by=user_id).all()
    return render_template("user.html", user=user, posts=posts)

@user_bp.route ('/users/<user_id>/edit')
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('edit-user.html', user=user)

@user_bp.route('/users/<user_id>/edit', methods=['POST'])
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

@user_bp.route('/users/<user_id>/posts/new')
def show_post_form(user_id):
    user = User.query.get(user_id)
    return render_template('new-post.html',user=user)


@user_bp.route('/posts/<post_id>')
def get_post(post_id):
    post = Post.query.get(post_id)
    author = db.session.query(User).filter(User.id == post.created_by).all()
    return render_template('post.html', post=post, author=author)

@user_bp.route('/posts/<post_id>/edit')
def edit_form_for_post(post_id):
    post = Post.query.get(post_id)
    return render_template('edit-post.html', post=post)