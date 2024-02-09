from unittest import TestCase
from flask import Flask
from app.user_routes import user_bp
from app.post_routes import post_bp
from app.app import app
from app.models import Post, PostTag, db, User
from flask_sqlalchemy import SQLAlchemy 
import os

app = Flask(__name__)

os.environ['DB_USERNAME'] = 'N'
os.environ['DB_PASSWORD'] = ' '
os.environ['DB_NAME'] = 'test_users'
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.environ['DB_USERNAME']}:{os.environ['DB_PASSWORD']}@localhost/{os.environ['DB_NAME']}"

db.init_app(app)

app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
app.config['SECRET_KEY'] = 'abc123'


app.register_blueprint(user_bp)
app.register_blueprint(post_bp)

with app.app_context():
    db.drop_all()   
    db.create_all()

class UserViewsTestCase(TestCase):

    def setUp(self):
        with app.app_context():
            db.create_all()
            User.query.delete()
            user = User(first_name="John", last_name="Doe")
            db.session.add(user)
            db.session.commit()
            self.id= user.id

    def tearDown(self):
        with app.app_context():
            db.drop_all()   
            db.session.rollback()
            db.session.commit()

    def test_list_users(self):
        with app.app_context():
            with app.test_client() as client:
                resp = client.get("/", follow_redirects=True)
                html = resp.get_data(as_text=True)

                self.assertEqual(resp.status_code, 200)
                self.assertIn('John Doe', html)


    def test_get_user(self):
        with app.app_context():
            with app.test_client() as client:
                response = client.get("/users/1")
                html = response.get_data(as_text=True)

                self.assertEqual(response.status_code, 200)
                self.assertIn('User 1', html)
                self.assertIn('John', html)
                self.assertIn('Doe', html)

    def test_edit_user(self):
        with app.app_context():
            with app.test_client() as client:
                response = client.get("/users/1/edit")
                html = response.get_data(as_text=True)

                self.assertEqual(response.status_code, 200)
                self.assertIn('User 1', html)
                self.assertIn('John', html)
                self.assertIn('Doe', html)
                self.assertIn('New first name', html)
                self.assertIn('Delete user?', html)

    def test_update_user(self):
        with app.app_context():
            with app.test_client() as client:
                response = client.post("/users/1/edit", data={
                    "newFirst": "Jane",
                    "newLast": "Smith",
                    "newImg": " ",
                }, follow_redirects=True)
                html = response.get_data(as_text=True)

                self.assertEqual(response.status_code, 200)

    def test_delete_user(self):
         with app.app_context():
            with app.test_client() as client:
                response = client.post("/users/1/delete", follow_redirects=True)
                html = response.get_data(as_text=True)
                self.assertEqual(response.status_code, 200)

class PostViewsTestCase(TestCase):
    def setUp(self):
        with app.app_context():
            db.create_all()
            User.query.delete()
            user = User(first_name="John", last_name="Doe")
            db.session.add(user)
            db.session.commit()
            Post.query.delete()
            post = Post(title="Test", content="Test Content")
            db.session.add(post)
            db.session.commit()
            self.id= post.id

    def tearDown(self):
        with app.app_context():
            db.drop_all()   
            db.session.rollback()
            db.session.commit()

    def test_add_post(self):
        with app.app_context():
            with app.test_client() as client:
                response = client.post("/users/1/posts/new", data={
                    "title": "Test",
                    "content": "test",
                }, follow_redirects=True)
                html = response.get_data(as_text=True)

                self.assertEqual(response.status_code, 200)
    
    def test_edit_post(self):
        with app.app_context():
            with app.test_client() as client:
                response = client.post("/posts/1/edit", data={
                    "newTitle": "apples",
                    "newContent": "oranges",
                }, follow_redirects=True)
                html = response.get_data(as_text=True)

                self.assertEqual(response.status_code, 200)
                self.assertIn('apples', html)
                self.assertIn('oranges', html)

    def test_delete_post(self):
         with app.app_context():
            with app.test_client() as client:
                response = client.post("/posts/1/delete", follow_redirects = True)
                html = response.get_data(as_text=True)

                self.assertEqual(response.status_code, 200)

    def test_get_post(self):
        with app.app_context():
            with app.test_client() as client:
                response = client.get("/posts/1", follow_redirects=True)
                html = response.get_data(as_text=True)
                self.assertEqual(response.status_code, 200)
                self.assertIn('Test', html)
                self.assertIn('Test Content', html)
    
    def test_edit_form_for_post(self):
        with app.app_context():
            with app.test_client() as client:
                response = client.get("/posts/1/edit", follow_redirects=True)
                html = response.get_data(as_text=True)
                self.assertEqual(response.status_code, 200)
                self.assertIn('Title', html)
                self.assertIn('Content', html)
    
def TagViewsTestCase(TestCase):
    def setUp(self):
        with app.app_context():
            db.create_all()
            User.query.delete()
            user = User(first_name="John", last_name="Doe")
            db.session.add(user)
            db.session.commit()
            Post.query.delete()
            post = Post(title="Test", content="Test Content")
            db.session.add(post)
            db.session.commit()
            

    def tearDown(self):
        with app.app_context():
            db.drop_all()   
            db.session.rollback()
            db.session.commit()

    def test_edit_tag(self):
        with app.app_context():
            with app.test_client() as client:

                response = client.post("/tags/1/edit",data={"newTag": "Banana"}, follow_redirects=True)
                html = response.get_data(as_text=True)
                self.assertEqual(response.status_code, 200)
                self.assertIn('Banana', html)

    def test_add_tag(self):
        with app.app_context():
            with app.test_client() as client:
                response = client.post("/tags/new", data={"newTag": "Banana"},follow_redirects=True)
                html = response.get_data(as_text=True)
                self.assertEqual(response.status_code, 200)
                self.assertIn('Banana', html)
                self.assertIn('Tags', html)

    def test_get_tag(self):
        with app.app_context():
            with app.test_client() as client:
                response = client.get("/tags/1/", follow_redirects=True)
                html = response.get_data(as_text=True)
                self.assertEqual(response.status_code, 200)
                self.assertIn('Test', html)


    def test_delete_tag(self):
        with app.app_context():
            with app.test_client() as client:
                response = client.post("/tags/1/delete", follow_redirects=True)
                html = response.get_data(as_text=True)
                self.assertEqual(response.status_code, 200)

def PostViewsTestCase(TestCase):
    def setUp(self):
        with app.app_context():
            db.create_all()
            User.query.delete()
            user = User(first_name="John", last_name="Doe")
            db.session.add(user)
            db.session.commit()
            Post.query.delete()
            post = Post(title="Test", content="Test Content")
            db.session.add(post)
            db.session.commit()
            post_tag = PostTag(1,1)
            db.session.add(post_tag)
            db.session.commit()
            

    def tearDown(self):
        with app.app_context():
            db.drop_all()   
            db.session.rollback()
            db.session.commit()

    def test_find_posts(self):
        with app.app_context():
            with app.test_client() as client:
                response = client.get("/tags/1", follow_redirects=True)
                html = response.get_data(as_text=True)
                self.assertEqual(response.status_code, 200)
                self.assertIn('1', html)
    