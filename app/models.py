from datetime import datetime
from flask_sqlalchemy import SQLAlchemy 

db = SQLAlchemy()

class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.Text, nullable=True, default='')

    posts = db.relationship('Post', backref='user', cascade='all, delete-orphan')

    @classmethod
    def __repr__(self):
        return f"<User id:{self.id} {self.first_name} {self.last_name}>"
    
class Post(db.Model):

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), default=1)

    # Connects Post to PostTag
    tagged_posts = db.relationship('PostTag', backref='post', cascade='all, delete-orphan')

    # "Through" relationship to posts_tags
    tags = db.relationship('Tag', secondary="posts_tags", backref="posts")

    @classmethod
    def __repr__(self):
        return f"<Post id:{self.id} {self.title} {self.content} {self.created_at}>"
    
class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False, unique=True)

    # Connect Tag to PostTag
    tagged_posts = db.relationship('PostTag', backref='tag')

class PostTag(db.Model):
    __tablename__ = 'posts_tags'
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True, nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True, nullable = False)