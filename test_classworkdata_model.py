from unittest import TestCase
from models import db, Student, School, Teacher, IEP, Goal, ClassworkData
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

        self.iep = IEP(student_id = self.stu.id,
            teacher_id=self.tch.id)

        db.session.add(self.iep)
        db.session.commit()

        self.goal = Goal(iep_id = self.iep.id,
            goal="Increase CWPM to 23",
            standard="Read with fluency")

        db.session.add(self.goal)
        db.session.commit()

        self.cw_data = ClassworkData(goal_id=self.goal.id,
            baseline="12 CWPM",
            current="15 CWPM",
            attainment="23 CWPM")

        db.session.add(self.cw_data)
        db.session.commit()

    def tearDown(self):
        db.session.rollback()
        Teacher.query.delete()
        School.query.delete()
        IEP.query.delete()
        Goal.query.delete()

    def test_cwdata_model(self):
        cw_data = ClassworkData.query.get(self.goal.id)
        self.assertEqual(self.cw_data.baseline, cw_data.baseline)
        self.assertEqual(self.cw_data.current, cw_data.current)
        self.assertEqual(self.cw_data.attainment, cw_data.attainment)
