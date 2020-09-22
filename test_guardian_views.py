from unittest import TestCase
from models import db, Guardian
from app import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres4@localhost/iep-test'

db.drop_all()
db.create_all()

app.config['WTF_CSRF_ENABLED'] = False

class TeacherViewTestCase(TestCase):

    def setUp(self):

        Guardian.query.delete()

        self.client = app.test_client()

        self.guardian = Guardian(first_name='Maria',
            last_name='Aldapa',
            relation='Aunt',
            username='mariaa',
            password='pizza123')

        self.data = {
            'first_name': self.guardian.first_name,
            'last_name': self.guardian.last_name,
            'relation': self.guardian.relation,
            'username': self.guardian.username,
            'password': self.guardian.password,
            'confirm': self.guardian.password
        }

    def tearDown(self):
        db.session.rollback()

    def test_teacher_registration_view(self):
        resp = self.client.post('/guardian/register',
            data=self.data,
            follow_redirects=True)
        html = resp.get_data(as_text=True)
        self.assertIn(self.guardian.first_name, html)

    def test_user_authentication_views(self):
        self.client.post('/guardian/register',
            data=self.data,
            follow_redirects=True)
        data = {
            'username': self.guardian.username,
            'password': self.guardian.password
        }
        resp = self.client.post('/guardian/login',
            data = data,
            follow_redirects=True)
        html = resp.get_data(as_text=True)

        self.assertIn(self.guardian.first_name, html)

    def test_user_auth_fail(self):
        data = {
            'username': 'Bad actor',
            'password': '%T^&*(%$#'
        }
        resp = self.client.post('/guardian/login', data = data, follow_redirects=True)
        html = resp.get_data(as_text=True)
        self.assertIn('Invalid username or password', html)