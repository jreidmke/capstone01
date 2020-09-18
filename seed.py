from app import db
from datetime import date
from models import School, Teacher, Student, Guardian, Family, IEP

db.drop_all()
db.create_all()

sch1 = School(name='Chicago')
sch2 = School(name='Geneva')
sch3 = School(name='Milwaukee')

db.session.add(sch1)
db.session.add(sch2)
db.session.add(sch3)

db.session.commit()

tch1 = Teacher(name='Jess Christensen', title='K4-2nd Sped', school_id = 1)
tch2 = Teacher(name='Tanya Scoma', title='3rd-5th Sped', school_id = 2)
tch3 = Teacher(name='Sally Krueger', title='Middle School Sped', school_id = 3)

db.session.add(tch1)
db.session.add(tch2)
db.session.add(tch3)

db.session.commit()

stu1 = Student(name='Fake Kid JR.', dob=date(2012, 1, 24), grade=1, teacher_id=1, dis_area='OHI')
stu2 = Student(name="Fake Kid", dob=date(2010, 4, 27), grade=4, teacher_id=2, dis_area='SDD')
stu3 = Student(name="Cool Dude", dob=date(2011, 7, 2), grade=8, teacher_id=3, dis_area='SLD')
stu4 = Student(name="Cool Dude JR", dob=date(2011, 7, 12), grade=2, teacher_id=1, dis_area='SLD')
stu5 = Student(name="Superman", dob=date(2011, 7, 12), grade=5, teacher_id=2, dis_area='EBD')
stu6 = Student(name="Batman", dob=date(2011, 7, 12), grade=6, teacher_id=3, dis_area='EBD')

db.session.add(stu1)
db.session.add(stu2)
db.session.add(stu3)
db.session.add(stu4)
db.session.add(stu5)
db.session.add(stu6)

db.session.commit()

par1 = Guardian(name='Fake Mom', relation='Mother')
par2 = Guardian(name='Fake Dad', relation='Father')
par3 = Guardian(name='Fake Aunt', relation='Aunt')
par4 = Guardian(name='Fake Brother', relation='Brother')

db.session.add(par1)
db.session.add(par2)
db.session.add(par3)
db.session.add(par4)

db.session.commit()

fam1 = Family(student_id=1, guardian_id=1)
fam2 = Family(student_id=1, guardian_id=2)
fam3 = Family(student_id=2, guardian_id=3)
fam4 = Family(student_id=3, guardian_id=4)

db.session.add(fam1)
db.session.add(fam2)
db.session.add(fam3)
db.session.add(fam4)

db.session.commit()

iep1 = IEP(student_id=1, teacher_id=1)
iep2 = IEP(student_id=2, teacher_id=2)
iep3 = IEP(student_id=3, teacher_id=3)
iep4 = IEP(student_id=4, teacher_id=1)
iep5 = IEP(student_id=5, teacher_id=2)
iep6 = IEP(student_id=6, teacher_id=3)

db.session.add(iep1)
db.session.add(iep2)
db.session.add(iep3)
db.session.add(iep4)
db.session.add(iep5)
db.session.add(iep6)

db.session.commit()

goal1 = Goal(iep_id=1, goal='Pay attention for 10 minutes', standard='Retain focus')