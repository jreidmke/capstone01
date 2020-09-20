from unittest import TestCase
from models import db, Guardian
from app import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres4@localhost/iep-test'

db.drop_all()
db.create_all()

class GuardianModelTestCase(TestCase):

    def setUp(self):
        self.guardian = Guardian(first_name='Fake',
            last_name='Dad',
            relation='Dad',
            username='fakedad123',
            password='imfakedad')
        db.session.add(self.guardian)
        db.session.commit()
        self.reg_obj = Guardian.register(first_name=self.guardian.first_name,
            last_name=self.guardian.last_name,
            relation=self.guardian.relation,
            username=self.guardian.username,
            password=self.guardian.password)

    def tearDown(self):
        Guardian.query.delete()
        db.session.rollback()

    def test_guardian_model(self):
        guardian_db = Guardian.query.get(self.guardian.id)
        self.assertEqual(self.guardian.first_name, guardian_db.first_name)
        self.assertEqual(self.guardian.last_name, guardian_db.last_name)
        self.assertEqual(self.guardian.relation, guardian_db.relation)

    def test_guardian_registration(self):
        self.assertEqual(self.reg_obj.username, self.guardian.username)
        self.assertEqual(self.reg_obj.first_name, self.guardian.first_name)
        self.assertEqual(self.reg_obj.last_name, self.guardian.last_name)

    def test_guardian_authentication(self):
        auth_obj = Guardian.authenticate(self.guardian.username, self.guardian.password)
        self.assertEqual(auth_obj, self.reg_obj)

    def test_failed_user_authentication(self):
        auth_obj = Guardian.authenticate('TESTUSER', 'foo')
        self.assertEqual(auth_obj, False)
