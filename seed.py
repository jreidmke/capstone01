from app import db
from datetime import date
from models import School, Teacher, Student, Guardian, Family, IEP, Goal, ClassworkData

db.drop_all()
db.create_all()

sch1 = School(name='Chicago',
    state='Illinois',
    state_code='549159D28465455FB144F5B67F3ACDFF')
sch2 = School(name='Minneapolis',
    state='Minnesota',
    state_code="B632FB4B1B83445AA8DB46DC3F079D19")
sch3 = School(name='Milwaukee',
    state='Wisconsin',
    state_code='745124D969E9491C9FC33D3235259386')

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

stu1 = Student(first_name='Oliver',
    last_name='Gee',
    dob=date(2012, 1, 24),
    grade=2,
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
    dis_area='OHI'
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

iep1 = IEP(student_id=1, teacher_id=1, date=date(2019, 9, 2))
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

goal1 = Goal(iep_id=1,
    goal='Pay attention for 10 minutes',
    standard_set_title='Illinois Learning Standards for Social/Emotional Development',
    standard_set_id='549159D28465455FB144F5B67F3ACDFF_D2406942_grades-01-02-03-k',
    standard_text='Demonstrate appropriate social and classroom behavior.',
    standard_id='A39873C0DFE5013184DB68A86D17958E')
goal2 = Goal(iep_id=1,
    goal='Correct display table data',
    standard_set_title='Illinois Learning Standards for Mathematics',
    standard_set_id='549159D28465455FB144F5B67F3ACDFF_D10001EB_grades-01-02-03-k',
    standard_text='Collect, organize and describe data using pictures, tallies, tables, charts or bar graphs.',
    standard_id='9D9C07D0DFE50131799768A86D17958E')
goal3 = Goal(iep_id=1,
    goal='Categorize words to demonstrate knowledge',
    standard_set_title='Illinois Learning Standards Incorporating the Common Core English Language Arts',
    standard_set_id='549159D28465455FB144F5B67F3ACDFF_D2418244_grade-01',
    standard_text='Sort words into categories (e.g., colors, clothing) to gain a sense of the concepts the categories represent.',
    standard_id='9F522BB0DFE501317CCA68A86D17958E')

goal4 = Goal(iep_id=7,
    goal='Identify and follow classroom rules',
    standard_set_title='Illinois Learning Standards Incorporating the Common Core English Language Arts',
    standard_set_id='549159D28465455FB144F5B67F3ACDFF_D2406942_grades-01-02-03-k',
    standard_text='Identify social norms and safety considerations that guide behavior.',
    standard_id='A39A6A00DFE5013184E268A86D17958E')
goal5 = Goal(iep_id=7,
    goal='Display knowledge of symmetry.',
    standard_set_title='Illinois Learning Standards for Mathematics',
    standard_set_id='549159D28465455FB144F5B67F3ACDFF_D10001EB_grades-01-02-03-k',
    standard_text='Identify lines of symmetry in simple figures and construct symmetrical figures using various concrete materials.',
    standard_id='9DA559F0DFE5013179A368A86D17958E')

goal6 = Goal(iep_id=7,
    goal='Do the work',
    standard_set_title="Illinois Learning Standards Incorporating the Common Core English Language Arts",
    standard_set_id="549159D28465455FB144F5B67F3ACDFF_D2418244_grade-02",
    standard_text='Draw evidence from literary or informational texts to support analysis, reflection, and research.',
    standard_id='9FB25AE0DFE501317D1768A86D17958E')


# goal4 = Goal(iep_id=2, goal='Read a whole book', standard='Reading')
# goal5 = Goal(iep_id=2, goal='Finish math problems', standard='Math')

# goal6 = Goal(iep_id=3, goal='Finish math problems', standard='Math')
# goal7 = Goal(iep_id=4, goal='Finish math problems', standard='Math')
# goal8 = Goal(iep_id=4, goal='Pay attention for 10 minutes', standard='Retain focus')
# goal9 = Goal(iep_id=5, goal='Do the work', standard='Work completion')
# goal10 = Goal(iep_id=6, goal='Do the work', standard='Work completion')

# goal11 = Goal(iep_id=7, goal='Pay attention for 10 minutes', standard='Retain focus')
# goal12 = Goal(iep_id=7, goal='Do the work', standard='Work completion')
# goal13 = Goal(iep_id=7, goal='Do the work', standard='Work completion')

db.session.add(goal1)
db.session.add(goal2)
db.session.add(goal3)
db.session.add(goal4)
db.session.add(goal5)
db.session.add(goal6)
# db.session.add(goal7)
# db.session.add(goal8)
# db.session.add(goal9)
# db.session.add(goal10)
# db.session.add(goal11)
# db.session.add(goal12)
# db.session.add(goal13)
db.session.commit()

cd1 = ClassworkData(goal_id=1, baseline='2 mins on task', current='3 1/2 mins on task', attainment='7 mins on task')
cd2 = ClassworkData(goal_id=2, baseline='20% completion', current='35% completion', attainment='60% completion')
cd3 = ClassworkData(goal_id=3, baseline='3/20 pgs read', current='3/20 pgs read', attainment='20 pgs read')
cd4 = ClassworkData(goal_id=4, baseline='3/20 pgs read', current='3/20 pgs read', attainment='20 pgs read')
cd5 = ClassworkData(goal_id=5, baseline='20% completion', current='35% completion', attainment='60% completion')
cd6 = ClassworkData(goal_id=6, baseline='20% completion', current='35% completion', attainment='60% completion')



# cd7 = ClassworkData(goal_id=7, baseline='20% completion', current='35% completion', attainment='60% completion')
# cd8 = ClassworkData(goal_id=8, baseline='2 mins on task', current='3 1/2 mins on task', attainment='7 mins on task')
# cd9 = ClassworkData(goal_id=9, baseline='20% of work', current='15% of work', attainment='60% of work')
# cd10 = ClassworkData(goal_id=10, baseline='20% of work', current='15% of work', attainment='60% of work')
# cd11 = ClassworkData(goal_id=11, baseline='2 mins on task', current='3 1/2 mins on task', attainment='7 mins on task')
# cd12 = ClassworkData(goal_id=12, baseline='20% completion', current='35% completion', attainment='60% completion')
# cd13 = ClassworkData(goal_id=13, baseline='3/20 pgs read', current='3/20 pgs read', attainment='20 pgs read')

db.session.add(cd1)
db.session.add(cd2)
db.session.add(cd3)
db.session.add(cd4)
db.session.add(cd5)
db.session.add(cd6)
# db.session.add(cd7)
# db.session.add(cd8)
# db.session.add(cd9)
# db.session.add(cd10)
# db.session.add(cd11)
# db.session.add(cd12)
# db.session.add(cd13)

db.session.commit()