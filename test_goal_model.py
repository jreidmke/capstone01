from unittest import TestCase
from models import db, Student, School, Teacher, IEP, Goal
from app import app
from datetime import date

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres4@localhost/iep-test'

db.drop_all()
db.create_all()

class GoalModelTestCase(TestCase):
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

        self.goal = Goal(iep_id = self.iep.id,
            goal="Increase CWPM to 23",
            standard="Read with fluency")

        db.session.add(self.goal)
        db.session.commit()

    def tearDown(self):
        db.session.rollback()
        Teacher.query.delete()
        School.query.delete()
        IEP.query.delete()
        Goal.query.delete()

    def test_goal_model(self):
        goal = Goal.query.get(self.goal.id)
        self.assertEqual(self.goal.goal, goal.goal)
        self.assertEqual(self.goal.standard, goal.standard)
        self.assertEqual(self.goal.iep_id, self.iep.id)