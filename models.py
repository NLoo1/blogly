from datetime import datetime
from flask_sqlalchemy import SQLAlchemy 

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

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
    created_by = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))

    # user = db.relationship('User', backref='posts', cascade='all')

    @classmethod
    def __repr__(self):
        return f"<Post id:{self.id} {self.title} {self.content} {self.created_at}>"