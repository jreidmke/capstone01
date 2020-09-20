from unittest import TestCase
from models import db, School
from app import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres4@localhost/iep-test'

db.drop_all()
db.create_all()

class SchoolModelTestCase(TestCase):
    """Test school model functions"""

    def setUp(self):
        self.school1 = School(name='Coultrap')
        self.school2 = School(name="Chicago")


    def tearDown(self):
        db.session.rollback()
        School.query.delete()


    def test_school_model(self):
        db.session.add(self.school1)
        db.session.add(self.school2)
        db.session.commit()
        school1 = School.query.get(self.school1.id)
        school2 = School.query.get(self.school2.id)
        self.assertEqual(self.school1.name, school1.name)
        self.assertEqual(self.school2.name, school2.name)
