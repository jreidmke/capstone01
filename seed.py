from app import db
from datetime import date
from random import uniform

from models import School, Teacher, Student

def get_random_datetime(year_gap=2):
    """Get a random datetime within the last few years."""

    now = datetime.now()
    then = now.replace(year=now.year - year_gap)
    random_timestamp = uniform(then.timestamp(), now.timestamp())

    return datetime.fromtimestamp(random_timestamp)

db.drop_all()
db.create_all()

sch1 = School(name='Chicago')
sch2 = School(name='Geneva')
sch3 = School(name='Milwaukee')

db.session.add(sch1)
db.session.add(sch2)
db.session.add(sch3)

db.session.commit()

tch1 = Teacher(name='Jess Christensen', title='4th Grade Teacher', school_id = 1)
tch2 = Teacher(name='Tanya Scoma', title='4th Grade Teacher', school_id = 2)
tch3 = Teacher(name='Sally Krueger', title='2nd Grade Teacher', school_id = 3)

db.session.add(tch1)
db.session.add(tch2)
db.session.add(tch3)

std1 = Student(name='Joe Boy', dob= date(2012, 1, 24))

db.session.add(std1)

db.session.commit()
