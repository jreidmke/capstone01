from flask import Flask, request, session, render_template, redirect, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from models import db, connect_db, School, Teacher, Student, Guardian, Family, IEP, Goal, ClassworkData
from forms import TeacherRegisterForm, GuardianRegisterForm

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres4@localhost/iep'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
app.config["SECRET_KEY"] = "abc123"

connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)

def login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id

@app.route('/teacher/register', methods=["GET", "POST"])
def show_teacher_reg():
    form = TeacherRegisterForm()

    if form.validate_on_submit():
        try:
            teacher = Teacher.register(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                title=form.title.data,
                school_id=form.school_id.data,
                username=form.username.data,
                password=form.password.data
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'bad')
            return render_template('teacher-reg.html', form=form)

        login(teacher)

        return redirect(f'/teacher/{teacher.id}')

    return render_template('teacher-reg.html', form=form)

@app.route('/teacher/<int:teacher_id>')
def show_teacher_detail(teacher_id):
    teacher = Teacher.query.get(teacher_id)
    return render_template('teacher-detail.html', teacher=teacher)

@app.route('/guardian/register', methods=["GET", "POST"])
def show_guardian_reg():
    form = GuardianRegisterForm()

    if form.validate_on_submit():
        try:
            guardian = Guardian.register(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                relation=form.relation.data,
                username=form.username.data,
                password=form.password.data
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'bad')
            return render_template('teacher-reg.html', form=form)

        login(guardian)

        return redirect(f'/guardian/{guardian.id}')

    return render_template('guardian-reg.html', form=form)

@app.route('/teacher/<int:guardian_id>')
def show_guardian_detail(guardian_id):
    guardian = Teacher.query.get(guardian_id)
    return render_template('guardian-detail.html', guardian=guardian)

@app.route('/student/id')
def show_student_detail():
    # flash('Welcome {Parent Name}', 'good')
    return render_template('student-detail.html')