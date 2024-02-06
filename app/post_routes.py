from datetime import datetime
import pdb
from flask import Blueprint, flash, redirect, render_template, request
from .models import PostTag, Tag, User, Post, db

post_bp = Blueprint('post_bp', __name__)

@post_bp.route('/users/<user_id>/edit', methods=['POST'])
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

@post_bp.route ('/users/<user_id>/delete', methods=['POST'])
def delete_user(user_id):
    Post.query.filter_by(user_id=user_id).delete()
    User.query.filter_by(id=user_id).delete()
    db.session.commit()
    flash('User deleted.')
    return redirect('/')

@post_bp.route ('/users/new', methods=['POST'])
def create_user():
    new_first = request.form['first_name']
    new_last = request.form['last_name']
    new_image = request.form['image_url']

    new_user = User(first_name=new_first,last_name=new_last,image_url=new_image)
    db.session.add(new_user)
    db.session.commit()

    return redirect("/")

# POSTS ------------------

@post_bp.route('/users/<user_id>/posts/new', methods=['POST'])
def add_post(user_id):
    title = request.form['title']
    content = request.form['content']
    time = datetime.now()
    new_post = Post(title=title,content=content,created_at=time,user_id=user_id)
    db.session.add(new_post)
    db.session.commit()

    tags = request.form.to_dict()

    for tag_name in tags:
        tag = Tag.query.filter_by(name=tag_name).first()

        # If value is tag:
        if tag:
            post_id = db.session.query(Post).filter_by(title=new_post.title,content=new_post.content).first().id
            new_tag = PostTag(post_id=post_id,tag_id=tag.id)
            db.session.add(new_tag)
            db.session.commit()
        else:
            continue

    return redirect("/")    

@post_bp.route('/posts/<post_id>/edit', methods=['POST'])
def edit_post(post_id):
    existing_post = Post.query.get(post_id)

    title = request.form['newTitle']
    content = request.form['newContent']


    # Update the existing user's properties
    existing_post.title = title
    existing_post.content = content

    db.session.add(existing_post)
    db.session.commit()

    # Clear all tags
    db.session.query(PostTag).filter_by(post_id=post_id).delete()
    db.session.commit()

    tags = request.form.to_dict()

    
    # Go through tags
    for tag_name in tags:
        try:
            tag = db.session.query(Tag).filter_by(name=tag_name).first()
            new_posttag = PostTag(post_id=post_id,tag_id=tag.id)
            db.session.add(new_posttag)
            db.session.commit()
        except(Exception):
            continue

    return redirect(f'/posts/{post_id}')

@post_bp.route('/posts/<post_id>/delete', methods=['POST'])
def delete_post(post_id):

    # Delete post_tag entry for relevant post
    PostTag.query.filter_by(post_id=post_id).delete()
    Post.query.filter_by(id=post_id).delete()
    db.session.commit()
    flash('Post deleted.')
    return redirect('/')

#  NEW TAGS ----------------------

@post_bp.route('/tags/new', methods=['POST'])
def new_tag():
    tag = request.form['newTag']
    tag = Tag(name=tag)
    db.session.add(tag)
    db.session.commit()
    return redirect('/tags')

@post_bp.route('/tags/<tag_id>/edit', methods=['POST'])
def edit_tag(tag_id):
    tag = Tag.query.get(tag_id)
    newTag = request.form['newTag']
    tag.name = newTag
    db.session.add(tag)
    db.session.commit()
    return redirect('/tags')

@post_bp.route('/tags/<tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    User.query.filter_by(id=tag_id).delete()
    db.session.commit()
    flash('Tag deleted.')
    return redirect('/')