from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo
from wtforms.fields.html5 import DateField


class TeacherRegisterForm(FlaskForm):
    """Form for registering as a teacher"""

    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    title = StringField('Title (Ex. 1st-2nd Sped Teacher)', validators=[DataRequired()])
    school_id = StringField('School', validators=[DataRequired()])
    username = StringField('User Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Confirm Password')

class GuardianRegisterForm(FlaskForm):
    """Form for registering a guardian"""

    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    relation = StringField('Relation to Student (Ex. "Mother" or "Uncle")', validators=[DataRequired()])
    username = StringField('User Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Confirm Password')

class StudentRegisterForm(FlaskForm):
    """For for registering student"""

    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    dob = DateField('Date of Birth (Format: M/D/YYYY)', validators=[DataRequired()])
    grade = IntegerField('Grade (Ex. 1 or 10)', validators=[DataRequired()])
    dis_area = SelectField('Disability Area', choices=['OHI', 'SDD', 'SLD', 'SLP', 'EBD', 'OI', 'ID', 'Autism'], validators=[DataRequired()])


class LoginForm(FlaskForm):
    """Form for teacher or guardian login"""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class FamilyForm(FlaskForm):
    """Form for teachers to create families"""

    parent_first_name = StringField('Parent First Name', validators=[DataRequired()])
    parent_last_name = StringField('Parent Last Name', validators=[DataRequired()])
    parent_username = StringField('Parent Username', validators=[DataRequired()])
    student_first_name = StringField('Student First Name', validators=[DataRequired()])
    student_last_name = StringField('Student Last Name', validators=[DataRequired()])
