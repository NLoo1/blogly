from unittest import TestCase

from app import app
from flask import session

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!

    def test_home(self):
        with app.test_client() as client:
            # with client.session_transaction() as change_session:
            #     change_session['count'] = 3
            #     change_session['playTimes'] = 3
           
            res = client.get('/')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)


