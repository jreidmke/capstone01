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
        self.tch1 = Teacher(first_name='Jess',
            last_name='Christensen',
            title='K4-2nd Sped',
            school_id=self.school.id,
            username='jessc',
            password='packers123')

        db.session.add(self.tch1)
        db.session.commit()

    def tearDown(self):
        db.session.rollback()
        Teacher.query.delete()
        School.query.delete()

    def test_teacher_model(self):
        tch1 = Teacher.query.get(self.tch1.id)
        self.assertEqual(self.tch1.first_name, tch1.first_name)
        self.assertEqual(self.tch1.last_name, tch1.last_name)
        self.assertEqual(self.tch1.title, tch1.title)
        self.assertEqual(self.tch1.school_id, tch1.school_id)