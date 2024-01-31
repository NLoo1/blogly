from unittest import TestCase
from flask import Flask
from user_routes import user_bp
from post_routes import post_bp
from app import app, connect_db
from models import db, User
from flask_sqlalchemy import SQLAlchemy 
import os

app = Flask(__name__)

os.environ['DB_USERNAME'] = 'N'
os.environ['DB_PASSWORD'] = ' '
os.environ['DB_NAME'] = 'test_users'
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.environ['DB_USERNAME']}:{os.environ['DB_PASSWORD']}@localhost/{os.environ['DB_NAME']}"

db.init_app(app)

app.config['SQLALCHEMY_ECHO'] = True
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

app.register_blueprint(user_bp)
app.register_blueprint(post_bp)

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

    def test_get_user(self):
        with self.app.test_request_context():
            response = self.client.get("/users/1")
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('User 1', html)
            self.assertIn('First name: John', html)
            self.assertIn('Last name: Doe', html)

    def test_edit_user(self):
        with self.app.test_request_context():
            response = self.client.get("/users/1/edit")
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('User 1', html)
            self.assertIn('First name: John', html)
            self.assertIn('Last name: Doe', html)
            self.assertIn('New first name', html)
            self.assertIn('Delete user?', html)

    def test_update_user(self):
        with self.app.test_request_context():
            response = self.client.post("/users/1/edit", data={
                "first_name": "Jane",
                "last_name": "Smith",
                "image_url": " ",
            }, follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)

    def test_delete_user(self):
        with self.app.test_request_context():
            response = self.client.post("/users/1/delete", follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)

