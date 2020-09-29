"""SQLAlchemy models"""

import datetime

from flask_bcrypt import Bcrypt
bc = Bcrypt()

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

def connect_db(app):
    """Connects application to database"""

    db.app = app
    db.init_app(app)

class School(db.Model):
    """School model"""

    __tablename__ = 'schools'

    id = db.Column(db.Integer,
        primary_key=True,
        autoincrement=True)
    name = db.Column(db.String,
        nullable=False)
    state = db.Column(db.String,
        nullable=False)
    state_code = db.Column(db.String,
        nullable=False)

class Teacher(db.Model):
    """Teacher model"""

    __tablename__ = 'teachers'

    id = db.Column(db.Integer,
        primary_key=True,
        autoincrement=True)
    first_name = db.Column(db.String,
        nullable=False)
    last_name = db.Column(db.String,
        nullable=False)
    title = db.Column(db.String,
        nullable=False)
    school_id = db.Column(db.Integer,
        db.ForeignKey('schools.id', ondelete='cascade'),
        nullable=False)
    username = db.Column(db.String(20),
        unique=True,
        nullable=False)
    password = db.Column(db.String,
        nullable=False)
    is_teacher = db.Column(db.Boolean,
        default=True)

    school = db.relationship('School')

    @classmethod
    def register(cls, first_name, last_name, title, school_id, username, password):
        """Creates new user with hased password"""

        hashword = bc.generate_password_hash(password).decode('utf8')

        teacher = Teacher(first_name=first_name,
            last_name=last_name,
            title=title,
            school_id=school_id,
            username=username,
            password=hashword)

        db.session.add(teacher)
        db.session.commit()
        return teacher

    @classmethod
    def authenticate(cls, username, password):
        """Returns user object if password validated."""

        teacher = Teacher.query.filter_by(username=username).first()

        if teacher and bc.check_password_hash(teacher.password, password):
            return teacher
        else:
            return False

class Student(db.Model):
    """Student model"""

    __tablename__ = 'students'

    id = db.Column(db.Integer,
        primary_key=True,
        autoincrement=True)
    first_name = db.Column(db.String,
        nullable=False)
    last_name = db.Column(db.String,
        nullable=False)
    dob = db.Column(db.Date,
        nullable=False) # in python datetime.date format
    grade = db.Column(db.Integer,
        nullable=False)
    teacher_id = db.Column(db.Integer,
        db.ForeignKey('teachers.id', ondelete='set null'))
    dis_area = db.Column(db.String,
        nullable=False)

    teacher = db.relationship('Teacher')

    guardians = db.relationship('Family', cascade='all, delete', backref='student')
    ieps = db.relationship('IEP', backref='student')

class Family(db.Model):
    """Family model"""

    __tablename__ = 'families'

    guardian_id = db.Column(db.Integer,
        db.ForeignKey('guardians.id', ondelete="cascade"),
        primary_key=True,
        nullable=False)
    student_id = db.Column(db.Integer,
        db.ForeignKey('students.id', ondelete="cascade"),
        primary_key=True,
        nullable=False)

class Guardian(db.Model):
    """Guardian model"""

    __tablename__ = 'guardians'

    id = db.Column(db.Integer,
        primary_key=True,
        autoincrement=True)
    first_name = db.Column(db.String,
        nullable=False)
    last_name = db.Column(db.String,
        nullable=False)
    relation = db.Column(db.String,
        nullable=False)
    username = db.Column(db.String(20),
        unique=True,
        nullable=False)
    password = db.Column(db.String,
        nullable=False)
    is_teacher = db.Column(db.Boolean,
        default=False)

    students = db.relationship('Family', cascade='all, delete', backref='guardian')

    @classmethod
    def register(cls, first_name, last_name, relation, username, password):
        """Creates new user with hased password"""

        hashword = bc.generate_password_hash(password).decode('UTF-8')

        guardian = Guardian(first_name=first_name,
            last_name=last_name,
            relation=relation,
            username=username,
            password=hashword)

        db.session.add(guardian)
        db.session.commit()
        return guardian

    @classmethod
    def authenticate(cls, username, password):
        """Returns user object if password validated."""

        guardian = Guardian.query.filter_by(username=username).first()

        if guardian and bc.check_password_hash(guardian.password, password):
            return guardian
        else:
            return False

class IEP(db.Model):
    """IEP model"""

    __tablename__ = 'ieps'

    id = db.Column(db.Integer,
        primary_key=True,
        autoincrement=True)
    date = db.Column(db.Date,
        default=datetime.date.today())
    student_id = db.Column(db.Integer,
        db.ForeignKey('students.id', ondelete="cascade"),
        nullable=False)
    teacher_id = db.Column(db.Integer,
        db.ForeignKey('teachers.id', ondelete='cascade'),
        nullable=False)
    is_locked = db.Column(db.Boolean,
        nullable=False,
        default=False)

    teacher = db.relationship("Teacher", primaryjoin="IEP.teacher_id == Teacher.id")

class Goal(db.Model):
    """Goal Model"""

    __tablename__ = 'goals'

    id = db.Column(db.Integer,
        primary_key=True,
        autoincrement=True)
    iep_id = db.Column(db.Integer,
        db.ForeignKey('ieps.id', ondelete="cascade"),
        nullable=False)
    goal = db.Column(db.String,
        nullable=False)
    subject = db.Column(db.String,
        nullable=False)

    data = db.relationship('ClassworkData', backref='goal')
    standard = db.relationship('GoalStandard', backref='goal')
    standard_set = db.relationship('GoalStandardSet', backref='goal')

class GoalStandardSet(db.Model):
    """Here the teacher selects the standard set from which their standard originates"""
    goal_id = db.Column(db.Integer,
        db.ForeignKey('goals.id', ondelete='cascade'),
        primary_key=True)
    standard_set_title = db.Column(db.String,
        nullable=False)
    standard_set_id = db.Column(db.String,
        nullable=False)

class GoalStandard(db.Model):
    """Here the teacher selects the standard the student's goal is attached to"""
    goal_id = db.Column(db.Integer,
        db.ForeignKey('goals.id', ondelete='cascade'),
        primary_key=True)
    standard_text = db.Column(db.String,
        nullable=False)
    standard_id = db.Column(db.String,
        nullable=False)

class ClassworkData(db.Model):
    """Classwork Data model. For each goal, we will store the baseline
    (data pertaining to student's present level for goal), level of attainment
    (the level at which the student is considered to have met his or her goal),
    and current level (the level the student is currently at for goal, to be updated by teacher)"""

    __tablename__ = 'classwork_data'

    goal_id = db.Column(db.Integer,
        db.ForeignKey('goals.id', ondelete='cascade'),
        primary_key=True)
    baseline = db.Column(db.String,
        nullable=False)
    current = db.Column(db.String,
        nullable=False)
    current_data_date = db.Column(db.Date,
        default=datetime.date.today())
    attainment = db.Column(db.String,
        nullable=False)
