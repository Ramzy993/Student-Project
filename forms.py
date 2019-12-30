from flask_wtf import FlaskForm
from wtforms import (StringField, BooleanField, IntegerField, RadioField, SelectField, TextField, SubmitField)


class add_student_form(FlaskForm):
    fname = StringField('First Name:')
    # , render_kw={'class':'col-sm-2 col-form-label'})
    lname = StringField('Last Name:')
    major = StringField('Major:')
    submit = SubmitField('Add Student')


class upd_student_form(add_student_form):
    students = RadioField('Pick a Student:')
    submit = SubmitField('Update Student')


class add_course_form(FlaskForm):
    name = StringField('Course Name:')
    dept = StringField('Course Department:')
    submit = SubmitField('Add Course')


class upd_course_form(add_course_form):
    courses = RadioField('Pick a course:')
    submit = SubmitField('Update Course')


class add_mail_form(FlaskForm):
    students = RadioField('Pick a Student:')
    mail = StringField('Student Email:')
    submit = SubmitField('Add Email')


class show_student_form(FlaskForm):
    students = RadioField('Pick a Student:')
    submit = SubmitField('Show Options')


class upd_mail_form(add_mail_form):
    mails = RadioField('Pick a mail:')
    submit = SubmitField('Update Email')


class add_address_form(FlaskForm):
    students = RadioField('Pick a Student:')
    building = IntegerField('Building Number:')
    street = StringField('Street Name:')
    city = StringField('City Name:')
    zip_code = IntegerField('Zip Code:')
    submit = SubmitField('Add Address')


class upd_address_form(add_address_form):
    addresses = RadioField('Pick a addresses:')
    submit = SubmitField('Update Address')


class add_student_course_form(FlaskForm):
    students = RadioField('Pick a Student:')
    courses = RadioField('Pick a course:')
    status = BooleanField('Succeeded?')
    submit = SubmitField('Add Course Status')


class upd_student_course_form(add_student_course_form):
    submit = SubmitField('Update Course Status')


class del_student_form(FlaskForm):
    students = RadioField('Pick a Student:')
    submit = SubmitField('Remove Student')


class del_course_form(FlaskForm):
    courses = RadioField('Pick a course:')
    submit = SubmitField('Remove Course')

