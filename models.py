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