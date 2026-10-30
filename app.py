import os
from datetime import datetime as dt
from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Student, Major

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = (
    'sqlite:///' + os.path.join(app.instance_path, 'university.db')
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'beyond_course_scope'

db.init_app(app)


@app.route('/student/view')
def student_view_all():
    students = (
        Student.query.outerjoin(Major, Student.major_id == Major.major_id)
        .add_entity(Major)
        .order_by(Student.last_name, Student.first_name)
        .all()
    )
    return render_template('student_view_all.html', students=students)


@app.route('/student/view/<int:student_id>')
def student_view(student_id):
    student = Student.query.filter_by(student_id=student_id).first()
    majors = Major.query.order_by(Major.major).all()

    if student:
        return render_template(
            'student_entry.html',
            student=student,
            majors=majors,
            action='read'
        )

    flash('Student attempting to be viewed could not be found!', 'error')
    return redirect(url_for('student_view_all'))


@app.route('/student/create', methods=['GET', 'POST'])
def student_create():
    if request.method == 'GET':
        majors = Major.query.order_by(Major.major).all()
        return render_template(
            'student_entry.html',
            majors=majors,
            action='create'
        )

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form.get('email', '').strip()
    major_id = request.form['major_id']
    birth_date = request.form['birth_date']
    is_honors = 'is_honors' in request.form

    if not email or len(email) > 100:
        flash(
            'Please enter an email address of 100 characters or fewer.',
            'error'
        )
        return redirect(url_for('student_create'))

    student = Student(
        first_name=first_name,
        last_name=last_name,
        email=email,
        major_id=major_id,
        birth_date=dt.strptime(birth_date, '%Y-%m-%d'),
        is_honors=is_honors
    )

    db.session.add(student)
    db.session.commit()

    flash(f'{first_name} {last_name} was successfully added!', 'success')
    return redirect(url_for('student_view_all'))


@app.route('/student/update/<int:student_id>', methods=['GET', 'POST'])
def student_edit(student_id):
    student = Student.query.filter_by(student_id=student_id).first()

    if not student:
        flash('Student attempting to be edited could not be found!', 'error')
        return redirect(url_for('student_view_all'))

    if request.method == 'GET':
        majors = Major.query.order_by(Major.major).all()
        return render_template(
            'student_entry.html',
            student=student,
            majors=majors,
            action='update'
        )

    email = request.form.get('email', '').strip()

    if not email or len(email) > 100:
        flash(
            'Please enter an email address of 100 characters or fewer.',
            'error'
        )
        return redirect(url_for('student_edit', student_id=student_id))

    student.first_name = request.form['first_name']
    student.last_name = request.form['last_name']
    student.email = email
    student.major_id = request.form['major_id']
    student.birth_date = dt.strptime(
        request.form['birth_date'], '%Y-%m-%d'
    )
    student.num_credits_completed = request.form['num_credits_completed']
    student.gpa = request.form['gpa']
    student.is_honors = 'is_honors' in request.form

    db.session.commit()

    flash(
        f'{student.first_name} {student.last_name} was successfully updated!',
        'success'
    )
    return redirect(url_for('student_view_all'))


@app.route('/student/delete/<int:student_id>')
def student_delete(student_id):
    student = Student.query.filter_by(student_id=student_id).first()

    if student:
        student_name = f'{student.first_name} {student.last_name}'
        db.session.delete(student)
        db.session.commit()
        flash(f'{student_name} was successfully deleted!', 'success')
    else:
        flash('Delete failed! Student could not be found.', 'error')

    return redirect(url_for('student_view_all'))


@app.route('/')
def home():
    return redirect(url_for('student_view_all'))


if __name__ == '__main__':
    app.run()