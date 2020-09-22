from unittest import TestCase
from models import db, Teacher, School
from app import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres4@localhost/iep-test'

db.drop_all()
db.create_all()

app.config['WTF_CSRF_ENABLED'] = False

class TeacherViewTestCase(TestCase):

    def setUp(self):

        School.query.delete()
        Teacher.query.delete()

        self.client = app.test_client()

        self.school = School(name='Minnesota')

        db.session.add(self.school)
        db.session.commit()

        self.teacher = Teacher(first_name='Maria',
            last_name='Aldapa',
            title='Teacher',
            school_id=self.school.id,
            username='mariaa',
            password='pizza123')

        self.data = {
            'first_name': self.teacher.first_name,
            'last_name': self.teacher.last_name,
            'title': self.teacher.title,
            'school_id': self.teacher.school_id,
            'username': self.teacher.username,
            'password': self.teacher.password,
            'confirm': self.teacher.password
        }

    def tearDown(self):
        db.session.rollback()

    def test_teacher_registration_view(self):
        resp = self.client.post('/teacher/register',
            data=self.data,
            follow_redirects=True)
        html = resp.get_data(as_text=True)
        self.assertIn(self.teacher.first_name, html)

    def test_user_authentication_views(self):
        self.client.post('/teacher/register',
            data=self.data,
            follow_redirects=True)
        data = {
            'username': self.teacher.username,
            'password': self.teacher.password
        }
        resp = self.client.post('/teacher/login',
            data = data,
            follow_redirects=True)
        html = resp.get_data(as_text=True)

        self.assertIn(self.teacher.first_name, html)

    def test_user_auth_fail(self):
        data = {
            'username': 'Bad actor',
            'password': '%T^&*(%$#'
        }
        resp = self.client.post('/teacher/login', data = data, follow_redirects=True)
        html = resp.get_data(as_text=True)
        self.assertIn('Invalid username or password', html)