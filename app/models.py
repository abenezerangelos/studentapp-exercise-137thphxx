from enum import unique
from app import db
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

@login.user_loader
def load_user(id):
    return Student.query.get(int(id))
   

class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    coursenum = db.Column(db.String(3))  
    title = db.Column(db.String(150))
    major = db.Column(db.String(20), db.ForeignKey('major.name'))

    roster = db.relationship('Enrolled',back_populates="classenrolled")

    def __repr__(self):
        return '<Class id: {} - coursenum: {}��title: {}, major: {}>'.format(self.id,self.coursenum,self.title, self.major)

    def getTitle(self):
        return self.title
   
class Major(db.Model):
    name = db.Column(db.String(20), primary_key=True)
    department = db.Column(db.String(150))
    classes = db.relationship('Class',backref = 'coursemajor', lazy = 'dynamic')
    def __repr__(self):
        return '<Major name: {} - department: {}>'.format(self.name,self.department)

class Student (UserMixin, db.Model):
    id =db.Column(db.Integer, primary_key = True)
    username =db.Column(db.String(64),unique=True, index =True)
    password_hash =db.Column(db.String(128))
    firstname =db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    address=db.Column(db.String(200))
    email=db.Column(db.String(120),unique=True,index=True)
    last_seen = db.Column(db.DateTime,default=datetime.utcnow)
    classes = db.relationship('Enrolled',back_populates="studentenrolled")

    def _repr_ (self):| 
        return '<Student : {}---{}.{}.-{};>'.format (self.id, self.firstname, self.lastname, self.email)

    def set_ password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_ password(self, password):
        return check_password_hash(self.password_hash, password)

    def enroll(self,newclass):
        if not self.is_enrolled(newclass):
            newEnrollment = Enrolled( classenrolled = newclass)
            self.classes.append(newEnrollment)
            db.session.commit()


    def unenroll(self,oldclass):
        if self.is_enrolled(oldclass)
            curEnrollment = Enrolled.query.filter_by(studentid=self.id).filter_by(classid=oldclass.id).first()
            db.session.delete(curEnrollment)
            db. session.commit()


    def is_enrolled(self,newclass):
        return Enrolled.query.filter_by(studentid=self.id).filter_by(classid=newclass.id).count()

    def enrolledCourses(self):
        return self.classes

    def getEnrolmentDate(self, theclass):
        if self.is_enrolled(theclass):
            return Enrolled.query.filter_by(studentid=self.id).filter_by(classid=theclass.id).first().enrolldate
        else:
            return None


enrolled = db.Table('enrolled',
    db.Column('studentid', db.Integer, db.ForeignKey('student.id')),
    db.Column('classid', db.Integer, db.ForeignKey('class.id'))
)

class Enrolled(db.Model):
    studentid = db.Column(db.Integer, db.ForeignKey('student.id' ), primary_key=True)
    classid = db.Column(db.Integer, db.ForeignKey('class.id' ), primary_key=True)
    enrolldate = db.Column(db.DateTime, default=datetime.utcnow)
    studentenrolled = db.relationship('Student')
    classenrolled = db.relationship('Class')
    def _repr_(self):
        return '<Enrollment class:{} student:{} date: {}>'.format(self.classenrolled,self.studentenrolled, self.enrolldate)
