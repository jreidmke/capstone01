from unittest import TestCase
from models import db, Student, School, Teacher
from app import app
from datetime import date

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres4@localhost/iep-test'

db.drop_all()
db.create_all()

app.config['WTF_CSRF_ENABLED'] = False


class StudentModelTestCase(TestCase):
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

    def tearDown(self):
        db.session.rollback()
        Student.query.delete()
        Teacher.query.delete()
        School.query.delete()

    def test_student_model(self):
        stu = Student.query.get(self.stu.id)
        self.assertEqual(self.stu.first_name, stu.first_name)
        self.assertEqual(self.stu.last_name, stu.last_name)
        self.assertEqual(self.stu.dob, stu.dob)
        self.assertEqual(self.stu.dis_area, stu.dis_area)
        self.assertEqual(self.stu.teacher_id, self.tch.id)

    def test_add_student(self):
        stu = Student(first_name='Tim',
            last_name='Tommerson',
            dob=date(2012, 1, 24),
            grade=1,
            teacher_id=self.tch.id,
            dis_area='OHI')

        data = {
            'first_name': stu.first_name,
            'last_name': stu.last_name,
            'dob': '1/24/2012',
            'grade': stu.grade,
            'teacher_id': stu.teacher_id,
            'dis_area': stu.dis_area
        }

        resp = app.test_client().post(f'/teacher/{self.tch.id}/add-student', data=data, follow_redirects=True)
        html = resp.get_data(as_text=True)
        self.assertIn('Student', html)

        stud = Student.query.filter_by(first_name=stu.first_name).first()
        self.assertEqual(stu.first_name, stud.first_name)
        self.assertEqual(stu.last_name, stud.last_name)
        self.assertEqual(stu.dob, stud.dob)
        self.assertEqual(stu.dis_area, stud.dis_area)
