from flask import Flask, request, session, render_template, redirect, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from models import db, connect_db, School, Teacher, Student, Guardian, Family, IEP, Goal, ClassworkData
from forms import TeacherRegisterForm, GuardianRegisterForm, LoginForm, StudentRegisterForm, FamilyForm
from datetime import date

CURR_USER_KEY = "current_user"

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


# Landing page.

@app.route('/')
def show_landing_page():
    return render_template('landing-page.html')

# Teacher Routing. Register and Login.

@app.route('/teacher/login', methods=["GET", "POST"])
def teacher_login():
    form = LoginForm()

    if form.validate_on_submit():
        teacher = Teacher.authenticate(form.username.data,
            form.password.data)

        if teacher:
            login(teacher)
            flash(f"Welcome {teacher.first_name}!", "good")
            return redirect(f"/teacher/{teacher.id}")

        flash("Invalid username or password", "bad")

    return render_template("login/teacher-login.html", form=form)

@app.route('/teacher/register', methods=["GET", "POST"])
def teacher_reg():
    form = TeacherRegisterForm()

    if form.validate_on_submit():

        # right here. check if school id is valid.
        id = form.school_id.data

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
            return render_template('register/teacher-reg.html', form=form)

        login(teacher)

        return redirect(f'/teacher/{teacher.id}')

    return render_template('register/teacher-reg.html', form=form)

@app.route('/teacher/<int:teacher_id>')
def show_teacher_detail(teacher_id):
    teacher = Teacher.query.get(teacher_id)
    students = Student.query.filter_by(teacher_id=teacher_id).all()
    if session[CURR_USER_KEY] == teacher.id:
        return render_template('teacher/teacher-detail.html', teacher=teacher, students=students)
    else:
        flash("You are not authorized to see this account", "bad")
        return redirect ('/teacher/login')

# Guardian Routing. Register and Login.

@app.route('/guardian/login', methods=["GET", "POST"])
def guardian_login():
    form = LoginForm()

    if form.validate_on_submit():
        guardian = Guardian.authenticate(form.username.data,
            form.password.data)

        if guardian:
            login(guardian)
            flash(f"Welcome {guardian.first_name}!", "good")
            return redirect(f"/guardian/{guardian.id}")

        flash("Invalid username or password", "bad")

    return render_template("login/guardian-login.html", form=form)

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

        except IntegrityError:
            flash("Username already taken", 'bad')
            return render_template('register/teacher-reg.html', form=form)

        login(guardian)

        return redirect(f'/guardian/{guardian.id}')

    return render_template('register/guardian-reg.html', form=form)

@app.route('/guardian/<int:guardian_id>')
def show_guardian_detail(guardian_id):
    guardian = Guardian.query.get(guardian_id)
    return render_template('guardian/guardian-detail.html', guardian=guardian)

@app.route('/student/id')
def show_student_detail():
    # flash('Welcome {Parent Name}', 'good')
    return render_template('student-detail.html')

@app.route('/teacher/<int:teacher_id>/add-student', methods=["GET", "POST"])
def add_student(teacher_id):
    teacher = Teacher.query.get(teacher_id)
    form = StudentRegisterForm()
    if form.validate_on_submit():
        student = Student(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            dob=form.dob.data,
            grade=form.grade.data,
            teacher_id=teacher_id,
            dis_area=form.dis_area.data
        )

        db.session.add(student)
        db.session.commit()

        return redirect(f'/teacher/{teacher_id}')

    return render_template('teacher/add-student.html', form=form, teacher=teacher)

@app.route('/teacher/<int:teacher_id>/add-family', methods=["GET", "POST"])
def add_family(teacher_id):
    teacher = Teacher.query.get(teacher_id)
    form = FamilyForm()
    if form.validate_on_submit():
        guardian = Guardian.query.filter_by(
            first_name=form.guardian_first_name.data,
            last_name=form.guardian_last_name.data,
            username=form.guardian_username.data).first()
        student = Student.query.filter_by(
            first_name=form.student_first_name.data,
            last_name=form.student_last_name.data).first()
        family = Family(
            guardian_id=guardian.id,
            student_id=student.id
        )


        db.session.add(family)
        db.session.commit()
        flash(f"Family created! Guardian {guardian.first_name} {guardian.last_name}, Student: {student.first_name} {student.last_name}!", "good")
        return redirect(f'/teacher/{teacher_id}')


    return render_template('/teacher/add-family.html', form=form, teacher=teacher)

@app.route('/student/<int:student_id>')
def show_student_detail(student_id):
    student = Student.query.get(student_id)
    return render_template()