"""Seed file to make sample data for db."""

from datetime import datetime
from models import db, User, Post
from app import app

# Create all tables
with app.app_context():
    db.drop_all()
    db.create_all()

    # Make a bunch of users
    user1 = User(first_name="John", last_name="Doe")
    user2 = User(first_name="Jane", last_name="Smith")
    user3 = User(first_name="Nick", last_name="Loo")

    db.session.add_all([user1, user2, user3])
    db.session.commit()

    # Make a bunch of posts
    post1 = Post(title="Dog", content="Check out this dog!", created_at=datetime.now(), created_by=1)
    post2 = Post(title="Cat", content="Check out this cat!", created_at=datetime.now(), created_by=1)
    post3 = Post(title="Apple", content="Check out this apple!", created_at=datetime.now(), created_by=2)
    post4 = Post(title="Orange", content="Check out this orange!", created_at=datetime.now(), created_by=2)
    post5 = Post(title="potato", content="Check out this potato!", created_at=datetime.now(), created_by=3)
    post6 = Post(title="tomato", content="Check out this tomato!", created_at=datetime.now(), created_by=3)

    db.session.add_all([post1, post2, post3, post4, post5, post6])
    db.session.commit()
