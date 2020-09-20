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
        guardian = Guardian(first_name='Fake',
            last_name='Dad',
            relation='Dad',
            username='fakedad123',
            password='imfakedad')
        db.session.add(guardian)
        db.session.commit()
        guardian_db = Guardian.query.get(guardian.id)
        self.assertEqual(guardian.first_name, guardian_db.first_name)
        self.assertEqual(guardian.last_name, guardian_db.last_name)
        self.assertEqual(guardian.relation, guardian_db.relation)
