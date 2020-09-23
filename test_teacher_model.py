from unittest import TestCase
from models import db, Teacher, School
from app import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres4@localhost/iep-test'

db.drop_all()
db.create_all()

class TeacherModelTestCase(TestCase):
    """Test teacher model functions"""

    def setUp(self):
        self.school = School(name='Coultrap')
        db.session.add(self.school)
        db.session.commit()

        self.tch = Teacher(first_name='Jess',
            last_name='Christensen',
            title='K4-2nd Sped',
            school_id=self.school.id,
            username='jessc',
            password='packers123')

        self.reg_obj = Teacher.register(first_name=self.tch.first_name,
            last_name=self.tch.last_name,
            title=self.tch.title,
            school_id=self.tch.school_id,
            username=self.tch.username,
            password=self.tch.password)

    def tearDown(self):
        db.session.rollback()
        Teacher.query.delete()
        School.query.delete()

    def test_guardian_registration(self):
        self.assertEqual(self.reg_obj.username, self.tch.username)
        self.assertEqual(self.reg_obj.first_name, self.tch.first_name)
        self.assertEqual(self.reg_obj.last_name, self.tch.last_name)

    def test_guardian_authentication(self):
        auth_obj = Teacher.authenticate(self.tch.username, self.tch.password)
        self.assertEqual(auth_obj, self.reg_obj)

    def test_failed_user_authentication(self):
        auth_obj = Teacher.authenticate('TESTUSER', 'foo')
        self.assertEqual(auth_obj, False)