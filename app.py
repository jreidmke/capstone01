from flask import Flask, request, session, render_template, redirect, flash
import requests
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from models import db, connect_db, School, Teacher, Student, Guardian, Family, IEP, Goal, ClassworkData, GoalStandard, GoalStandardSet, MsgToTeacher, MsgToGuardian
from forms import TeacherRegisterForm, GuardianRegisterForm, LoginForm, StudentRegisterForm, FamilyForm, GoalForm, ClassworkDataForm, CurrentClassworkDataForm, StandardSetForm, StandardForm, MsgToTeacherForm, MsgToGuardianForm
from datetime import date
from operator import itemgetter

# from wtforms_components import SelectWidget

CURR_USER_KEY = "current_user"
IS_TEACHER = "is_teacher"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres4@localhost/iep'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
app.config["SECRET_KEY"] = "abc123"

connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)

def get_state_codes():
    states = requests.get('http://commonstandardsproject.com/api/v1/jurisdictions/').json()['data']
    data = [standards for standards in states if standards["type"] == "state"]
    return data

def get_standards_list(state_code):
    standards = requests.get(f'http://commonstandardsproject.com/api/v1/jurisdictions/{state_code}').json()['data']['standardSets']
    return standards

def get_subject_list(standards):
    subject_list = [standard_subject["subject"] for standard_subject in standards]
    return subject_list

def get_grade_level_standard_sets(grade, standards):
    """Returns all State Grade Level Standard Sets per grade in arguemnt
    Organized by subject."""

    grade_level_standards = [standard for standard in standards if grade in standard['educationLevels']]

    return grade_level_standards

def sort_sets_by_subject(subject_list, standard_set_list):
    standard_sets_by_subject = {}

    for subject in subject_list:
        sub_list = []
        for obj in standard_set_list:
            if subject == obj["subject"]:
                sub_list.append({'title': obj["document"]["title"],
                    'id': obj["id"]})

            standard_sets_by_subject[subject] = sub_list

    return standard_sets_by_subject



def get_standards(standard_set_code):
    standards = requests.get(f'http://commonstandardsproject.com/api/v1/standard_sets/{standard_set_code}').json()['data']['standards']

    standard_id_list = standards.keys()

    des = []
    for id in standard_id_list:
        des.append(standards[id]['description'])

    standards_dict = dict(zip(des, standard_id_list))

    return standards_dict


def append_zero_convert_to_string(int):
    """The API formats single digit grades as strings with appended 0's (ex. 02, 07, 08)"""
    if int <= 9:
        return ('0' + str(int))
    else:
        return str(int)


def login(user):
    """Log in user."""
    session[CURR_USER_KEY] = user.id
    session[IS_TEACHER] = user.is_teacher

def logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

    if IS_TEACHER in session:
        del session[IS_TEACHER]


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

@app.route('/logout')
def logout_user():
    logout()
    return redirect('/')

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
    if session[CURR_USER_KEY] == teacher.id and session[IS_TEACHER] == True:
        return render_template('teacher/teacher-detail.html', teacher=teacher, students=students)
    else:
        flash("You are not authorized to see this account", "bad")
        return redirect ('/teacher/login')

@app.route('/teacher/<int:teacher_id>/add-student', methods=["GET", "POST"])
def add_student(teacher_id):
    if teacher_id == session[CURR_USER_KEY] and session[IS_TEACHER] == True:
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
        else:
            return render_template('teacher/add-student.html', form=form)
    else:
        flash("You are not authorized to view this account", "bad")
        return redirect('/')

@app.route('/teacher/<int:teacher_id>/add-family', methods=["GET", "POST"])
def add_family(teacher_id):
    if teacher_id == session[CURR_USER_KEY] and session[IS_TEACHER] == True:
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
            flash(f"Family created! Guardian: {guardian.first_name} {guardian.last_name}, Student: {student.first_name} {student.last_name}!", "good")
            return redirect(f'/teacher/{session[CURR_USER_KEY]}')
        students = Student.query.all()
        guardians = Guardian.query.all()
        return render_template('/teacher/add-family.html', form=form, students=students, guardians=guardians)

#************************************************
#************************************************
# Guardian Routing. Register and Login.
#************************************************
#************************************************

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
    family = Family.query.filter_by(guardian_id=guardian.id).all()
    return render_template('guardian/guardian-detail.html', guardian=guardian)

@app.route('/guardian/<int:guardian_id>/new-message/student/<int:student_id>', methods=["GET", "POST"])
def to_teacher_message(guardian_id, student_id):
    guardian = Guardian.query.get(guardian_id)
    student = Student.query.get(student_id)
    iep = IEP.query.filter_by(student_id=student.id).order_by(IEP.id.desc()).first()

    goals = Goal.query.filter_by(iep_id=iep.id).all()

    if session[IS_TEACHER] == False and session[CURR_USER_KEY] == guardian_id:
        form = MsgToTeacherForm()

        if form.validate_on_submit():
            msg = MsgToTeacher()


    flash('You are not authorized to view this page.')
    return redirect('/guardian/login')


#************************************************
#************************************************
# Student Routing.
#************************************************
#************************************************

@app.route('/student/<int:student_id>')
def show_student_detail(student_id):

    student = Student.query.get(student_id)

    teacher_id = student.teacher.id
    if teacher_id == session[CURR_USER_KEY] and session[IS_TEACHER] == True:
        latest_iep = IEP.query.filter_by(student_id=student.id).order_by(IEP.id.desc()).first()
        goals = Goal.query.filter_by(iep_id=latest_iep.id).all()
        guardians = Family.query.filter_by(student_id=student_id).all()
        ieps = IEP.query.filter_by(student_id=student_id).all()
        return render_template('/student/student-detail.html', student=student, guardians=guardians, ieps=ieps, latest_iep=latest_iep, goals=goals)
    else:
        flash('You are not authorized to view this page.')
        return redirect(f'/teacher/{teacher_id}')


# IEP Routing

@app.route('/student/<int:student_id>/iep')
def create_iep(student_id):
    iep = IEP(
        student_id=student_id,
        teacher_id=session[CURR_USER_KEY],
    )
    db.session.add(iep)
    db.session.commit()
    return redirect(f'/iep/{iep.id}/goal')

@app.route('/iep/<int:iep_id>/goal/', methods=["GET", "POST"])
def create_goal(iep_id):
    iep = IEP.query.get(iep_id)
    student = Student.query.get(iep.student_id)

    standards = get_standards_list(student.teacher.school.state_code)
    grade_level = get_grade_level_standard_sets(append_zero_convert_to_string(student.grade), standards)
    subject_list = get_subject_list(grade_level)

    g_form = GoalForm()
    d_form = ClassworkDataForm()

    g_form.subject.choices = subject_list

    goals = Goal.query.filter_by(iep_id=iep.id).all()

    if g_form.validate_on_submit() and d_form.validate_on_submit():
        goal = Goal(
            iep_id=iep.id,
            goal=g_form.goal.data,
            subject=g_form.subject.data
        )
        db.session.add(goal)
        db.session.commit()
        data = ClassworkData(
            goal_id=goal.id,
            baseline=d_form.baseline.data,
            current=d_form.baseline.data,
            attainment=d_form.attainment.data
        )
        db.session.add(data)
        db.session.commit()
        flash(f"Goal created! {goal.goal}. {data.baseline}. {data.attainment}. Select Standard Set", "good")
        return redirect(f'/goal/{goal.id}/standard_set')

    return render_template('/student/goal.html', g_form=g_form, d_form=d_form, student=student, iep_id=iep.id, goals=goals)

@app.route('/goal/<int:goal_id>/standard_set', methods=["GET", "POST"])
def select_standard_set(goal_id):

    goal = Goal.query.get(goal_id)
    iep = IEP.query.get(goal.iep_id)
    student = Student.query.get(iep.student_id)
    standards = get_standards_list(student.teacher.school.state_code)
    grade_level = get_grade_level_standard_sets(append_zero_convert_to_string(student.grade), standards)
    subject_list = get_subject_list(grade_level)

    standard_set = sort_sets_by_subject(subject_list, grade_level)

    selected_standard_set = standard_set[goal.subject]

    selected_standard_titles = [standard_set['title'] for standard_set in selected_standard_set]

    form = StandardSetForm()

    form.standard_set.choices=selected_standard_titles

    if form.validate_on_submit():
        standard_set_id = ''
        for standard in selected_standard_set:
            if standard['title'] == form.standard_set.data:
                standard_set_id = standard['id']


        standard_set = GoalStandardSet(goal_id=goal.id,
            standard_set_title = form.standard_set.data,
            standard_set_id = standard_set_id)
        db.session.add(standard_set)
        db.session.commit()
        flash(f'Standard Set Selected. {standard_set.standard_set_title}!', 'good')
        return redirect(f'/goal/{goal.id}/standard')

    return render_template('/student/standard-set.html', form=form)

@app.route('/goal/<int:goal_id>/standard', methods=["POST", "GET"])
def select_standard(goal_id):
    goal = Goal.query.get(goal_id)
    standard_set = GoalStandardSet.query.get(goal.id)

    standards = get_standards(standard_set.standard_set_id)

    standard_text = list(standards.keys())

    form = StandardForm()

    form.standard.choices = standard_text

    if form.validate_on_submit():
        standard = GoalStandard(goal_id=goal.id,
            standard_text=form.standard.data,
            standard_id=standards[form.standard.data])

        db.session.add(standard)
        db.session.commit()
        flash(f'{standard.standard_text}', 'good')
        return redirect(f'/iep/{goal.iep_id}/goal/')

    return render_template('/student/select-standard.html', form=form)

@app.route('/student/<int:student_id>/iep/<int:iep_id>')
def show_iep(student_id, iep_id):
    student = Student.query.get(student_id)
    teacher_id = student.teacher.id
    guardians = Family.query.filter_by(student_id=student_id).all()
    guardians = [guardian.guardian_id for guardian in guardians]

    if (session[IS_TEACHER] == False and session[CURR_USER_KEY] in guardians) or (session[IS_TEACHER] == True and session[CURR_USER_KEY] == teacher_id):
        iep = IEP.query.get(iep_id)
        goals = Goal.query.filter_by(iep_id=iep.id).all()
        return render_template('student/iep-detail.html', student=student, iep=iep, goals=goals)
    else:
        flash('You are not authorized to view this page.')
        return redirect(f'/teacher/{teacher_id}')

@app.route('/goal/<int:goal_id>/data', methods=["GET", "POST"])
def set_current_data(goal_id):
    form = CurrentClassworkDataForm()
    goal = Goal.query.get(goal_id)
    iep = IEP.query.get(goal.iep_id)
    data = ClassworkData.query.filter_by(goal_id=goal.id).first()

    if form.validate_on_submit():
        data.current = form.current.data

        db.session.add(data)
        db.session.commit()
        flash(f'Data updated for goal: {goal.goal}', "good")
        return redirect(f'/student/{iep.student_id}/iep/{iep.id}')

    return render_template('/student/current-data.html', goal=goal, data=data, form=form)

@app.route('/goal/<int:goal_id>/edit', methods=["GET", "POST"])
def edit_goal_page(goal_id):
    goal = Goal.query.get(goal_id)
    iep = IEP.query.get(goal.iep.id)

    teacher = Teacher.query.get(goal.iep.teacher_id)
    if goal.iep.is_locked == True:
        flash('IEP is locked. Goals cannot be edited.', 'bad')
        return redirect(f'/teacher/{teacher.id}')

    student = Student.query.get(goal.iep.student_id)
    standards = get_standards_list(student.teacher.school.state_code)
    grade_level = get_grade_level_standard_sets(append_zero_convert_to_string(student.grade), standards)
    subject_list = get_subject_list(grade_level)

    g_form = GoalForm()
    d_form = ClassworkDataForm()

    g_form.subject.choices = subject_list

    if g_form.validate_on_submit() and d_form.validate_on_submit():

        Goal.query.filter_by(id=goal.id).delete()
        ClassworkData.query.filter_by(goal_id=goal.id).delete()
        goal = Goal(
            iep_id=iep.id,
            goal=g_form.goal.data,
            subject=g_form.subject.data
        )
        db.session.add(goal)
        db.session.commit()

        data = ClassworkData(
            goal_id=goal.id,
            baseline=d_form.baseline.data,
            current=d_form.baseline.data,
            attainment=d_form.attainment.data
        )
        db.session.add(data)
        db.session.commit()


        # goal.goal = g_form.goal.data
        # goal.subject = g_form.subject.data
        # db.session.add(goal)
        # db.session.commit()

        # cw_data.baseline = d_form.baseline.data
        # cw_data.current = d_form.baseline.data
        # cw_data.attainment = d_form.attainment.data
        # db.session.add(cw_data)
        # db.session.commit()

        flash(f"Goal updated!", "good")
        return redirect(f'/goal/{goal.id}/standard_set')

    return render_template('/student/edit-goal.html', g_form=g_form, d_form=d_form)

@app.route('/iep/<int:iep_id>/lock')
def lock_iep(iep_id):
    iep = IEP.query.get(iep_id)
    iep.is_locked=True
    db.session.add(iep)
    db.session.commit()
    student = Student.query.get(iep.student_id)
    flash('IEP locked')
    return redirect(f'/student/{student.id}/iep/{iep.id}')