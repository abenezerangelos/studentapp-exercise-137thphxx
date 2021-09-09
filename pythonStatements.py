

from app import db
from app.models import Student, Class, enrolled
from datetime import datetime

db.create.all()

c1 = Class.query.filter_by(coursenum = '321').filter_by(major='Cpts').first()
c2 = Class.query.filter_by(coursenum = '322').filter_by(major='CptS').first()
c3 = Class.query.filter_by(coursenum = '355').filter_by(major='CptS').first()
c4 = Class.query.filter_by(coursenum = '451').filter_by(major='Cpts').first()

s1= Student.query.filter_by(username= 'sakire').first()


s1.classes.append(c2)
s1.classes.append(c3)
s1.classes.append(c4)
db.session.commit()

s1.classes.remove(c4)
db.session.commit()

# import db models
from c in s1.classes:
    print(c)

#create class objects and write them to the database

enrolledClasses = Class.query.join(enrolled,(enrolled.c.classid == Class.id)).filter_by(enrolled.c.studentid == s1.id).order_by(Class.coursenum).all()

#checkif-the  student is-enrolled-in a-given-class
s1.classes.filter(enrolled.c.classid == c2.id).count() > 0

#we can¡¤also ¡¤add ¡¤students to-a-class' :roster
s2 = Student.query.filter_by(username='john').first()
c2.roster.append(s2)
db.session.commit()

for c in s2.classes:
    print(c)
for s in c2.roster:
    print(s)

