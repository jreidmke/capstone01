"""SQLAlchemy models"""

from datetime import datetime

# from flask_bcrypt import Bcrypt
# bcrypt = Bcrypt()

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class School(db.Model):
    """School model"""

    __tablename__ = 'schools'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)


class Teacher(db.Model):
    """Teacher model"""

    __tablename__ = 'teachers'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    school_id = db.Column(db.Integer, db.ForeignKey('schools.id', ondelete='cascade'), nullable=False)

class Student(db.Model):
    """Student model"""

    __tablename____ = 'students'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    dob = db.Column(db.DateTime, nullable=False) # in YY, MM, DD format


def connect_db(app):
    """Connects application to database"""

    db.app = app
    db.init_app(app)