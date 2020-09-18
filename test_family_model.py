from unittest import TestCase
from models import db, Student, School, Teacher, Guardian, Family
from app import app
from datetime import date

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres4@localhost/iep-test'

db.drop_all()
db.create_all()

class FamilyModelTestCase(TestCase):
    """Test student model functions"""

    def setUp(self):
        self.school = School(name='Florida')
        db.session.add(self.school)
        db.session.commit()

        self.tch = Teacher(name='Jess Christensen',
            title='K4-2nd Sped',
            school_id = self.school.id)
        db.session.add(self.tch)
        db.session.commit()

        self.stu = Student(name='Fake Kid JR.',
            dob=date(2012, 1, 24),
            grade=1,
            teacher_id=self.tch.id,
            dis_area='OHI')
        db.session.add(self.stu)
        db.session.commit()

        self.guardian = Guardian(name='Fake Dad',
            relation='Dad')
        db.session.add(self.guardian)
        db.session.commit()

        self.family = Family(guardian_id=self.guardian.id,
            student_id=self.stu.id)

        db.session.add(self.family)
        db.session.commit()

    def tearDown(self):
        db.session.rollback()
        Teacher.query.delete()
        School.query.delete()
        Guardian.query.delete()
        Family.query.delete()

    def test_family_model(self):
        fam = Family.query.get((self.guardian.id, self.stu.id)) #Family model has multiple primary keys
        self.assertEqual(self.family.guardian_id, fam.guardian_id)
        self.assertEqual(self.family.student_id, fam.student_id)
