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

        self.guardian = Guardian(first_name='Fake',
            last_name='Dad',
            relation='Dad',
            username='fakedad123',
            password='imfakedad')
        self.guardian2 = Guardian(first_name='Fake',
            last_name='Mom',
            relation='Mom',
            username='fakemom123',
            password='imfakemom')
        db.session.add(self.guardian)
        db.session.add(self.guardian2)
        db.session.commit()

        self.family = Family(guardian_id=self.guardian.id,
            student_id=self.stu.id)
        self.family2 = Family(guardian_id=self.guardian2.id,
            student_id=self.stu.id)

        db.session.add(self.family)
        db.session.add(self.family2)
        db.session.commit()

    def tearDown(self):
        db.session.rollback()
        Teacher.query.delete()
        School.query.delete()
        Guardian.query.delete()
        Family.query.delete()

    def test_family_model(self):
        fam = Family.query.get((self.guardian.id, self.stu.id)) #Family model has multiple primary keys
        fam2 = Family.query.get((self.guardian2.id, self.stu.id))
        self.assertEqual(self.family.guardian_id, fam.guardian_id)
        self.assertEqual(self.family.student_id, fam.student_id)
        self.assertEqual(self.family2.guardian_id, fam2.guardian_id)
        self.assertEqual(self.family2.student_id, fam.student_id)
