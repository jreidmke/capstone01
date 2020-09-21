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