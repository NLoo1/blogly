from unittest import TestCase
from app import app
from models import db, User
from flask_sqlalchemy import SQLAlchemy 
import os

app.config['SQLALCHEMY_DATABASE_URI'] = ''
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

os.environ['DB_USERNAME'] = 'N'
os.environ['DB_PASSWORD'] = ' '
os.environ['DB_NAME'] = 'test_users'
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.environ['DB_USERNAME']}:{os.environ['DB_PASSWORD']}@localhost/{os.environ['DB_NAME']}"

with app.app_context():
    db.drop_all()
    db.create_all()

class UserViewsTestCase(TestCase):

    def setUp(self):
        with app.app_context():

            User.query.delete()
            user = User(first_name="John", last_name="Doe")
            db.session.add(user)
            db.session.commit()
            self.id= user.id

    def tearDown(self):
        with app.app_context():

            db.session.rollback()

    def test_list_users(self):
        with app.app_context():
            with app.test_client() as client:
                resp = client.get("/", follow_redirects=True)
                html = resp.get_data(as_text=True)

                self.assertEqual(resp.status_code, 200)
                self.assertIn('John Doe', html)