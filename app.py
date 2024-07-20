from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@localhost:3307/cmsc_447_individ_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Student(db.Model):
    studentID = db.Column(db.String(50), primary_key=True)
    studentName = db.Column(db.String(255), nullable=False)
    creditsEarned = db.Column(db.Integer)

class Instructor(db.Model):
    instructorID = db.Column(db.String(50), primary_key=True)
    instructorName = db.Column(db.String(255), nullable=False)
    courseDepartment = db.Column(db.String(100))

class Course(db.Model):
    courseID = db.Column(db.String(50), primary_key=True)
    courseTitle = db.Column(db.String(255), nullable=False)
    instructorID = db.Column(db.String(50), db.ForeignKey('instructor.instructorID'))
    courseCredits = db.Column(db.Integer)
    instructor = db.relationship('Instructor', backref='courses')

class Enrollment(db.Model):
    enrollmentID = db.Column(db.String(50), primary_key=True)
    studentID = db.Column(db.String(50), db.ForeignKey('student.studentID'))
    courseID = db.Column(db.String(50), db.ForeignKey('course.courseID'))
    studentCourseGrade = db.Column(db.String(2))
    student = db.relationship('Student', backref='enrollments')
    course = db.relationship('Course', backref='enrollments')

# Takes care of adding data to the tables in the database
@app.route('/add_item', methods=['POST'])
def add_item():
    data = request.json
    item_type = data.get('type')

    try:
        # Remove 'type' field from data
        data.pop('type', None)

        if item_type == 'Student':
            new_student = Student(**data)
            db.session.add(new_student)

        elif item_type == 'Instructor':
            new_instructor = Instructor(**data)
            db.session.add(new_instructor)

        elif item_type == 'Course':
            new_course = Course(**data)
            db.session.add(new_course)

        elif item_type == 'Enrollment':
            new_enrollment = Enrollment(**data)
            db.session.add(new_enrollment)

        else:
            return jsonify({'message': 'Invalid item type'}), 400

        db.session.commit()
        return jsonify({'message': f'{item_type} data added successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error: {str(e)}'}), 500

# Takes care of deleting data from the tables in the database
@app.route('/delete_item', methods=['POST'])
def delete_item():
    data = request.json
    item_type = data.get('type')

    try:
        if item_type == 'Student':
            student_id = data.get('studentID')
            student_name = data.get('studentName')
            credits_earned = data.get('creditsEarned')

            # Check if a student with the provided ID and other criteria exists
            student = Student.query.filter_by(studentID=student_id, studentName=student_name, creditsEarned=credits_earned).all()

            if student:
                # Check if the student is associated with any enrollments
                associated_enrollments = Enrollment.query.filter_by(studentID=student_id).all()

                if associated_enrollments:
                    # If there are associated enrollments, inform the user
                    return jsonify({'message': 'Student is enrolled in courses. Unenroll before deletion.'}), 400

                # If no associated enrollments, proceed with deletion
                db.session.delete(student)
                db.session.commit()
                return jsonify({'message': 'Student data deleted successfully'}), 200

            else:
                return jsonify({'message': 'Student not found'}), 404

        if item_type == 'Instructor':
            instructor_id = data.get('instructorID')
            instructor_name = data.get('instructorName')
            course_department = data.get('courseDepartment')

            # Check if an instructor with the provided ID and other criteria exists
            instructor = Instructor.query.filter_by(instructorID=instructor_id, instructorName=instructor_name, courseDepartment=course_department).all()

            if instructor:
                # Check if the instructor is associated with any courses
                associated_courses = Course.query.filter_by(instructorID=instructor_id).all()

                if associated_courses:
                    # If there are associated courses, inform the user
                    return jsonify({'message': 'Instructor is teaching courses. Unassign courses before deletion.'}), 400

                # If no associated courses, proceed with deletion
                db.session.delete(instructor)
                db.session.commit()
                return jsonify({'message': 'Instructor data deleted successfully'}), 200

            else:
                return jsonify({'message': 'Instructor not found'}), 404

        if item_type == 'Course':
            course_id = data.get('courseID')
            course_title = data.get('courseTitle')
            instructor_id = data.get('instructorID')
            course_credits = data.get('courseCredits')

            # Check if a course with the provided ID and other criteria exists
            course = Course.query.filter_by(courseID=course_id, courseTitle=course_title, instructorID=instructor_id, courseCredits=course_credits).all()

            if course:
                # Check if the course is associated with any enrollments
                associated_enrollments = Enrollment.query.filter_by(courseID=course_id).all()

                if associated_enrollments:
                    # If there are associated enrollments, inform the user
                    return jsonify({'message': 'Course has enrolled students. Unenroll students before deletion.'}), 400

                # If no associated enrollments, proceed with deletion
                db.session.delete(course)
                db.session.commit()
                return jsonify({'message': 'Course data deleted successfully'}), 200

            else:
                return jsonify({'message': 'Course not found'}), 404

        elif item_type == 'Enrollment':
            enrollment_id = data.get('enrollmentID')
            student_id = data.get('studentID')
            course_id = data.get('courseID')
            student_course_grade = data.get('studentCourseGrade')

            # Check if an enrollment with the provided ID and other criteria exists
            enrollment = Enrollment.query.filter_by(enrollmentID=enrollment_id, studentID=student_id, courseID=course_id, studentCourseGrade=student_course_grade).all()

            if enrollment:
                db.session.delete(enrollment)
                db.session.commit()
                return jsonify({'message': 'Enrollment data deleted successfully'}), 200
            else:
                return jsonify({'message': 'Enrollment not found'}), 404

        else:
            return jsonify({'message': 'Invalid item type'}), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error: {str(e)}'}), 500

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
