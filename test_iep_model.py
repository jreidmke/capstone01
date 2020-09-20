from unittest import TestCase
from models import db, Student, School, Teacher, IEP
from app import app
from datetime import date

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres4@localhost/iep-test'

db.drop_all()
db.create_all()

class FamilyModelTestCase(TestCase):
    """Test student model functions"""

    def setUp(self):
        self.school = School(name='Minnesota')
        db.session.add(self.school)
        db.session.commit()

        self.tch = Teacher(first_name='Jess',
            last_name='Christensen',
            title='K4-2nd Sped',
            school_id=self.school.id,
            username='jessc',
            password='packers123')
        db.session.add(self.tch)
        db.session.commit()

        self.stu = Student(first_name='Fake',
            last_name='Kid',
            dob=date(2012, 1, 24),
            grade=1,
            teacher_id=self.tch.id,
            dis_area='OHI')
        db.session.add(self.stu)
        db.session.commit()

        self.iep = IEP(student_id = self.stu.id,
            teacher_id=self.tch.id)

        db.session.add(self.iep)
        db.session.commit()

    def tearDown(self):
        db.session.rollback()
        Teacher.query.delete()
        School.query.delete()
        IEP.query.delete()

    def test_iep_model(self):
        iep = IEP.query.get(self.iep.id)
        self.assertEqual(self.iep.student_id, iep.student_id)
        self.assertEqual(self.iep.teacher_id, iep.teacher_id)