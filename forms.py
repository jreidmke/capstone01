from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo

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
    dob = DateField('Date of Birth', validators=[DataRequired()])
    grade = IntegerField('Grade (Ex. 1 or 10)', validators=[DataRequired()])
    # teacher_id =
    dis_area = StringField('Disability Area', validators=[DataRequired()])


class LoginForm(FlaskForm):
    """Form for teacher or guardian login"""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
