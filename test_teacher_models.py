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
        self.tch1 = Teacher(name='Jess Christensen', title='K4-2nd Sped', school_id = self.school.id)
        self.tch2 = Teacher(name='Tanya Scoma', title='3rd-5th Sped', school_id = self.school.id)
        self.tch3 = Teacher(name='Sally Krueger', title='Middle School Sped', school_id = self.school.id)
        db.session.add(self.tch1)
        db.session.add(self.tch2)
        db.session.add(self.tch3)
        db.session.commit()

    def tearDown(self):
        db.session.rollback()
        Teacher.query.delete()
        School.query.delete()

    def test_teacher_model(self):
        tch1 = Teacher.query.get(1)
        tch2 = Teacher.query.get(2)
        tch3 = Teacher.query.get(3)
        self.assertEqual(self.tch1.name, tch1.name)
        self.assertEqual(self.tch2.title, tch2.title)
        self.assertEqual(self.tch3.school_id, tch3.school_id)