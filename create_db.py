from app import app, db
from models import Student, Major
import datetime as dt
import os

with app.app_context():
    os.makedirs(app.instance_path, exist_ok=True)

    db.drop_all()
    db.create_all()

    # Initial loading of majors
    majors = [
        'Accounting',
        'Finance',
        'Information Systems',
        'International Business',
        'Management',
        'Operations Management & Business Analytics',
        'Supply Chain Management'
    ]

    for each_major in majors:
        print(each_major)
        a_major = Major(major=each_major)
        db.session.add(a_major)

    db.session.commit()

    # Initial loading of students
    students = [
        {
            'first_name': 'Robert',
            'last_name': 'Smith',
            'email': 'robert.smith@example.com',
            'major_id': 3,
            'birth_date': dt.datetime(2007, 6, 1),
            'is_honors': True
        },
        {
            'first_name': 'Leo',
            'last_name': 'Van Munching',
            'email': 'leo.vanmunching@example.com',
            'major_id': 6,
            'birth_date': dt.datetime(2008, 3, 24),
            'is_honors': False
        }
    ]

    for each_student in students:
        a_student = Student(
            first_name=each_student['first_name'],
            last_name=each_student['last_name'],
            email=each_student['email'],
            major_id=each_student['major_id'],
            birth_date=each_student['birth_date'],
            is_honors=each_student['is_honors']
        )
        db.session.add(a_student)
        print(
            f"{each_student['first_name']} "
            f"{each_student['last_name']} inserted into Student"
        )

    db.session.commit()
    print('Database created successfully!')