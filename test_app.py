# test_app.py
from app import create_app
from models import db, User
from unittest import TestCase

class UserViewsTestCase(TestCase):
    def setUp(self):
        self.app = create_app(testing=True)
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

            user = User(first_name="John", last_name="Doe")
            db.session.add(user)
            db.session.commit()
            self.id = user.id

    def tearDown(self):
        with self.app.app_context():
            db.session.rollback()
            db.drop_all()

    def test_list_users(self):
        with self.app.app_context():
            resp = self.client.get("/")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('John Doe', html)
