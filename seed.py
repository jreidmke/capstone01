import app
from models import School

sch1 = School(name='Christensen')
sch2 = School(name='Anderson')
sch3 = School(name='Milwaukee')

db.session.add(sch1)
db.session.add(sch2)
db.session.add(sch3)

db.session.commit()