import os

from flask import Flask, render_template, url_for, redirect
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from forms import add_student_form, add_course_form, add_mail_form, add_address_form, \
    add_student_course_form, upd_student_form, upd_course_form, upd_mail_form, upd_address_form,\
    upd_student_course_form, del_student_form, del_course_form, show_student_form

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)


##########################################
# SQL DATABASE AND MODELS
##########################################

class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.Text)
    lname = db.Column(db.Text)
    major = db.Column(db.Text)

    email = db.relationship('Email', backref='student')
    address = db.relationship('Address', backref='student', uselist=False)
    course = db.relationship('StudentCourse', backref='student')

    def __init__(self, fname, lname, major):
        self.fname = fname
        self.lname = lname
        self.major = major

    # def __repr__(self):
    #     return [self.id, self.fname, self.lname]


class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    department = db.Column(db.Text)

    def __init__(self, name, dept):
        self.name = name
        self.department = dept

    # def __repr__(self):
    #     return f"Course of {self.name} of department {self.department}"


class Email(db.Model):
    __tablename__ = 'emails'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    email = db.Column(db.Text)

    def __init__(self, email, student_id):
        self.email = email
        self.student_id = student_id

    def __repr__(self):
        return f"{self.email} "


class Address(db.Model):
    __tablename__ = 'addresses'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    building = db.Column(db.Integer)
    street = db.Column(db.Text)
    city = db.Column(db.Text)
    zip_code = db.Column(db.Integer)

    def __init__(self, building, street, city, zip_code, student_id):
        self.building = building
        self.street = street
        self.city = city
        self.zip_code = zip_code
        self.student_id = student_id

    def __repr__(self):
        return f"Student's address is building {self.building} {self.street} st. - {self.city} city, zip code:\
                {self.zip_code}"


class StudentCourse(db.Model):
    __tablename__ = 'students_courses'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    success_status = db.Column(db.Boolean)

    course = db.relationship('Course', backref='StudentCourse')

    def __init__(self, success_status, student_id, course_id):
        self.success_status = success_status
        self.student_id = student_id
        self.course_id = course_id

    def __repr__(self):
        return f"{self.course.name} - {self.course.department} - " + ("Succeeded" if self.success_status else "Not Succeeded")


##########################################
# VIEWS WITH FORMS
##########################################

def get_all_students():
    return [(student.id, student.fname.capitalize() + " " + student.lname.capitalize()) for student in
            Student.query.all()]


def get_all_students_info():
    return [(student.id, student.fname.capitalize() + " " + student.lname.capitalize(), student.major,
             ", ".join(repr(c) for c in student.course), ", ".join(repr(e) for e in student.email),
             student.address) for student in Student.query.all()]


def get_all_courses():
    return [(course.id, course.name.capitalize() + " - " + course.department.capitalize()) for course in
            Course.query.all()]


def get_all_courses_info():
    return [(course.id, course.name.capitalize(), course.department.capitalize()) for course in
            Course.query.all()]


def get_all_student_mails(student_id):
    return [(email.id, email.email) for email in
            Email.query.filter_by(student_id=student_id).all()]


@app.route('/')
def index():
    db.create_all()
    return render_template('Home.html')


@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    form = add_student_form()

    if form.validate_on_submit():

        fname = form.fname.data
        lname = form.lname.data
        major = form.major.data

        student = Student(fname, lname, major)
        db.session.add(student)
        db.session.commit()

        return redirect(url_for('add_student'))

    return render_template('Add.html', form=form, add_type='Student')


@app.route('/add_course', methods=['GET', 'POST'])
def add_course():
    form = add_course_form()

    if form.validate_on_submit():
        name = form.name.data
        dept = form.dept.data

        course = Course(name, dept)
        db.session.add(course)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('Add.html', form=form, add_type='Course')


@app.route('/add_email', methods=['GET', 'POST'])
def add_email():

    form = add_mail_form()
    form.students.choices = get_all_students()

    if form.is_submitted():

        mail = form.mail.data
        id_ = form.students.data

        mail = Email(mail, id_)
        db.session.add(mail)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('Add.html', form=form, add_type='Email')


@app.route('/add_address', methods=['GET', 'POST'])
def add_address():
    form = add_address_form()
    form.students.choices = get_all_students()

    if form.is_submitted():

        building = form.building.data
        street = form.street.data
        city = form.city.data
        zip_code = form.zip_code.data
        id_ = form.students.data

        address = Address(building, street, city, zip_code, id_)
        db.session.add(address)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('Add.html', form=form, add_type='Address')


@app.route('/add_student_course', methods=['GET', 'POST'])
def add_student_course():
    form = add_student_course_form()

    form.students.choices = get_all_students()
    form.courses.choices = get_all_courses()

    if form.is_submitted():

        student_id = form.students.data
        course_id = form.courses.data
        status = form.status.data

        student_course = StudentCourse(status, student_id, course_id)
        db.session.add(student_course)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('Add.html', form=form, add_type='Student Course')


@app.route('/upd_student', methods=['GET', 'POST'])
def upd_student():

    form = upd_student_form()
    form.students.choices = get_all_students()

    if form.is_submitted():
        student_id = form.students.data
        student = Student.query.get(student_id)
        student.fname = form.fname.data
        student.lname = form.lname.data
        student.major = form.major.data

        db.session.commit()

        return redirect(url_for('index'))

    return render_template('Update.html', form=form, upt_type='Student')


@app.route('/upd_course', methods=['GET', 'POST'])
def upd_course():

    form = upd_course_form()
    form.courses.choices = get_all_courses()

    if form.is_submitted():
        course_id = form.courses.data
        course = Student.query.get(course_id)
        course.name = form.name.data
        course.dept = form.dept.data

        db.session.commit()

        return redirect(url_for('index'))

    return render_template('Update.html', form=form, upt_type='Course')


@app.route('/upd_email', methods=['GET', 'POST'])
def upd_email():

    mail_form = upd_mail_form()
    mail_form.mails.choices = get_all_student_mails(1)
    form = show_student_form()
    form.students.choices = get_all_students()

    if form.is_submitted():

        mail_form.mails.choices = get_all_student_mails(form.students.data)

        if mail_form.is_submitted():
            email = Email.query.get(mail_form.mails.data)
            email.mail = mail_form.mail.data

            db.session.commit()

            return redirect(url_for('index'))

    return render_template('Update.html', form=form, option_form=mail_form, upt_type='Email')


@app.route('/del_student', methods=['GET', 'POST'])
def del_student():
    form = del_student_form()
    form.students.choices = get_all_students()

    if form.is_submitted():
        student_id = form.students.data
        Student.query.filter_by(id=student_id).delete()
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('Delete.html', form=form, del_type='Student')


@app.route('/del_course', methods=['GET', 'POST'])
def del_course():
    form = del_course_form()
    form.courses.choices = get_all_courses()

    if form.is_submitted():
        course_id = form.courses.data
        Course.query.filter_by(id=course_id).delete()
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('Delete.html', form=form, del_type='Course')


@app.route('/list_students', methods=['GET', 'POST'])
def list_students():
    return render_template('List.html', students=get_all_students_info(), List_type='Students')


@app.route('/list_courses', methods=['GET', 'POST'])
def list_courses():
    return render_template('List.html', courses=get_all_courses_info(), List_type='courses')


if __name__ == '__main__':
    app.run(debug=True)
