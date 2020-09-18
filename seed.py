from app import db
from datetime import date
from models import School, Teacher, Student, Guardian, Family

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

std1 = Student(name='Fake Kid JR.', dob=date(2012, 1, 24), grade=1, teacher_id=1, dis_area='OHI')
std2 = Student(name="Fake Kid", dob=date(2010, 4, 27), grade=4, teacher_id=2, dis_area='SDD')
std3 = Student(name="Cool Dude", dob=date(2011, 7, 2), grade=8, teacher_id=3, dis_area='SLD')

db.session.add(std1)
db.session.add(std2)
db.session.add(std3)

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