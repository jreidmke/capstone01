from app import db
from datetime import date
from models import School, Teacher, Student, Guardian, Family, IEP, Goal, ClassworkData

db.drop_all()
db.create_all()

sch1 = School(name='Chicago')
sch2 = School(name='Geneva')
sch3 = School(name='Milwaukee')

db.session.add(sch1)
db.session.add(sch2)
db.session.add(sch3)
db.session.commit()

Teacher.register(first_name='James',
    last_name='Reid',
    title='K4-2nd Sped',
    school_id=1,
    username='jreidmke',
    password='123'
    )
Teacher.register(first_name='Tanya',
    last_name='Scoma',
    title='3rd-5th Sped',
    school_id = 2,
    username='tanyas',
    password='badgers123'
    )
Teacher.register(first_name='Sally',
    last_name='Krueger',
    title='Middle School Sped',
    school_id=3,
    username='sallyk',
    password='zach123'
    )

stu1 = Student(first_name='Fake',
    last_name='Kid JR.',
    dob=date(2012, 1, 24),
    grade=1,
    teacher_id=1,
    dis_area='OHI'
    )
stu2 = Student(first_name="Fake",
    last_name="Kid",
    dob=date(2010, 4, 27),
    grade=4,
    teacher_id=2,
    dis_area='SDD'
    )
stu3 = Student(first_name="Cool",
    last_name="Dude",
    dob=date(2011, 7, 2),
    grade=8,
    teacher_id=3,
    dis_area='SLD'
    )
stu4 = Student(first_name="Cool",
    last_name="Dude JR",
    dob=date(2011, 7, 12),
    grade=2,
    teacher_id=1,
    dis_area='SLD'
    )
stu5 = Student(first_name="Superman",
    last_name="Kent",
    dob=date(2011, 7, 12),
    grade=5,
    teacher_id=2,
    dis_area='EBD'
    )
stu6 = Student(first_name="Batman",
    last_name="Wayne",
    dob=date(2011, 7, 12),
    grade=6,
    teacher_id=3,
    dis_area='EBD'
    )

db.session.add(stu1)
db.session.add(stu2)
db.session.add(stu3)
db.session.add(stu4)
db.session.add(stu5)
db.session.add(stu6)
db.session.commit()

par1 = Guardian.register(first_name='Fake',
    last_name='Mom',
    relation='Mother',
    username='fakemom123',
    password='iamfake'
    )
par2 = Guardian.register(first_name='Fake',
    last_name='Dad',
    relation='Father',
    username='fakedad123',
    password='iamfake'
    )
par3 = Guardian.register(first_name='Fake',
    last_name='Aunt',
    relation='Aunt',
    username='fakeaunt123',
    password='iamfake'
    )
par4 = Guardian.register(first_name='Fake',
    last_name='Brother',
    relation='Brother',
    username='fakebro',
    password='iamfake'
    )

fam1 = Family(student_id=1, guardian_id=1)
fam2 = Family(student_id=2, guardian_id=1)
fam5 = Family(student_id=1, guardian_id=2)
fam6 = Family(student_id=2, guardian_id=2)

fam3 = Family(student_id=2, guardian_id=3)
fam4 = Family(student_id=3, guardian_id=4)

db.session.add(fam1)
db.session.add(fam2)
db.session.add(fam3)
db.session.add(fam4)
db.session.add(fam5)
db.session.add(fam6)

db.session.commit()

iep1 = IEP(student_id=1, teacher_id=1)
iep2 = IEP(student_id=2, teacher_id=2)
iep3 = IEP(student_id=3, teacher_id=3)
iep4 = IEP(student_id=4, teacher_id=1)
iep5 = IEP(student_id=5, teacher_id=2)
iep6 = IEP(student_id=6, teacher_id=3)
iep7 = IEP(student_id=1, teacher_id=1)

db.session.add(iep1)
db.session.add(iep2)
db.session.add(iep3)
db.session.add(iep4)
db.session.add(iep5)
db.session.add(iep6)
db.session.add(iep7)
db.session.commit()

goal1 = Goal(iep_id=1, goal='Pay attention for 10 minutes', standard='Retain focus')
goal2 = Goal(iep_id=1, goal='Finish math problems', standard='Math')
goal3 = Goal(iep_id=1, goal='Read a whole book', standard='Reading')
goal4 = Goal(iep_id=2, goal='Read a whole book', standard='Reading')
goal5 = Goal(iep_id=2, goal='Finish math problems', standard='Math')
goal6 = Goal(iep_id=3, goal='Finish math problems', standard='Math')
goal7 = Goal(iep_id=4, goal='Finish math problems', standard='Math')
goal8 = Goal(iep_id=4, goal='Pay attention for 10 minutes', standard='Retain focus')
goal9 = Goal(iep_id=5, goal='Do the work', standard='Work completion')
goal10 = Goal(iep_id=6, goal='Do the work', standard='Work completion')

goal11 = Goal(iep_id=7, goal='Pay attention for 10 minutes', standard='Retain focus')
goal12 = Goal(iep_id=7, goal='Do the work', standard='Work completion')
goal13 = Goal(iep_id=7, goal='Do the work', standard='Work completion')

db.session.add(goal1)
db.session.add(goal2)
db.session.add(goal3)
db.session.add(goal4)
db.session.add(goal5)
db.session.add(goal6)
db.session.add(goal7)
db.session.add(goal8)
db.session.add(goal9)
db.session.add(goal10)
db.session.add(goal11)
db.session.add(goal12)
db.session.add(goal13)
db.session.commit()

cd1 = ClassworkData(goal_id=1, baseline='2 mins on task', current='3 1/2 mins on task', attainment='7 mins on task')
cd2 = ClassworkData(goal_id=2, baseline='20% completion', current='35% completion', attainment='60% completion')
cd3 = ClassworkData(goal_id=3, baseline='3/20 pgs read', current='3/20 pgs read', attainment='20 pgs read')
cd4 = ClassworkData(goal_id=4, baseline='3/20 pgs read', current='3/20 pgs read', attainment='20 pgs read')
cd5 = ClassworkData(goal_id=5, baseline='20% completion', current='35% completion', attainment='60% completion')
cd6 = ClassworkData(goal_id=6, baseline='20% completion', current='35% completion', attainment='60% completion')
cd7 = ClassworkData(goal_id=7, baseline='20% completion', current='35% completion', attainment='60% completion')
cd8 = ClassworkData(goal_id=8, baseline='2 mins on task', current='3 1/2 mins on task', attainment='7 mins on task')
cd9 = ClassworkData(goal_id=9, baseline='20% of work', current='15% of work', attainment='60% of work')
cd10 = ClassworkData(goal_id=10, baseline='20% of work', current='15% of work', attainment='60% of work')

cd11 = ClassworkData(goal_id=11, baseline='2 mins on task', current='3 1/2 mins on task', attainment='7 mins on task')
cd12 = ClassworkData(goal_id=12, baseline='20% completion', current='35% completion', attainment='60% completion')
cd13 = ClassworkData(goal_id=13, baseline='3/20 pgs read', current='3/20 pgs read', attainment='20 pgs read')

db.session.add(cd1)
db.session.add(cd2)
db.session.add(cd3)
db.session.add(cd4)
db.session.add(cd5)
db.session.add(cd6)
db.session.add(cd7)
db.session.add(cd8)
db.session.add(cd9)
db.session.add(cd10)
db.session.add(cd11)
db.session.add(cd12)
db.session.add(cd13)

db.session.commit()