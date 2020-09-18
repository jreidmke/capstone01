import os
from unittest import TestCase
from models import db, School
from app import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres4@localhost/iep-test'
db.create_all()

class SchoolModelTestCase(TestCase):
    """Test school model functions"""

    def setUp(self):
        """Create school"""
        self.school = School(name='Coultrap')

    def tearDown(self):
        db.session.rollback()

    def test_school_model(self):
        db.session.add(self.school)
        db.session.commit()
        school = School.query.get(1)
        self.assertEqual(self.school.name, school.name)