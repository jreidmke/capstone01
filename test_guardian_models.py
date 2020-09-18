from unittest import TestCase
from models import db, Guardian
from app import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres4@localhost/iep-test'

db.drop_all()
db.create_all()

class GuardianModelTestCase(TestCase):
    def test_guardian_model(self):
        Guardian.query.delete()
        db.session.rollback()
        guardian = Guardian(name='Fake Dad', relation='Dad')
        db.session.add(guardian)
        db.session.commit()
        guardian_db = Guardian.query.get(guardian.id)
        self.assertEqual(guardian.name, guardian_db.name)
        self.assertEqual(guardian.relation, guardian_db.relation)
