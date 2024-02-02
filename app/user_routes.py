import pdb
from flask import Blueprint, flash, redirect, render_template, request
from app.models import PostTag, Tag, User, Post, db


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
    posts = Post.query.filter_by(user_id=user_id).all()
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
    tags = Tag.query.all()
    return render_template('new-post.html',user=user, tags=tags)

# POSTS ----------------

@user_bp.route('/posts/<post_id>')
def get_post(post_id):
    post = Post.query.get(post_id)
    author = db.session.query(User).filter(User.id == post.user_id).all()
    tags = db.session.query(Tag).filter((PostTag.tag_id == Tag.id) & (PostTag.post_id == post_id)).all()
    return render_template('post.html', post=post, author=author, tags=tags)

@user_bp.route('/posts/<post_id>/edit')
def edit_form_for_post(post_id):
    post = Post.query.get(post_id)
    tags = Tag.query.all()
    checked_tags = db.session.query(Tag).filter((PostTag.tag_id == Tag.id) & (PostTag.post_id == post_id)).all()
    return render_template('edit-post.html', post=post, tags=tags, checked_tags=checked_tags)

# TAGS ---------------

@user_bp.route('/tags')
def get_tags():
    tags = Tag.query.all()
    return render_template('tags.html', tags=tags)

@user_bp.route('/tags/<tag_id>')
def get_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    # Get post IDs
    get_posts = db.session.query(PostTag).filter(PostTag.tag_id == tag_id).all()
    return render_template('tag.html', tag=tag, posts=get_posts)

@user_bp.route('/tags/new')
def new_tag_form():
    return render_template('new-tag.html')

@user_bp.route('/tags/<tag_id>/edit')
def edit_tag_form(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return render_template('edit-tag.html', tag=tag)