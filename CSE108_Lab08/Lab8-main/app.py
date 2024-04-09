from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin import BaseView
from flask_admin import expose
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite'
app.config['SECRET_KEY'] = 'mysecret'
database = SQLAlchemy(app)

class student(database.Model):      
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(80), unique=True, nullable=False)
    password = database.Column(database.String(120), nullable=False)
    firstname = database.Column(database.String(80), nullable=False)
    lastname = database.Column(database.String(80), nullable=False)
    enrollment = database.relationship('enrollment', backref='Student', lazy=True)

class teacher(database.Model):      
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(80), nullable=False, unique=True)
    password = database.Column(database.String(120), nullable=False)
    firstname = database.Column(database.String(80), nullable=False)
    lastname = database.Column(database.String(80), nullable=False)
    class_relation = database.relationship('classes', backref='Teacher', lazy=True)

class admin(database.Model):        
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(80), nullable=False, unique=True)
    password = database.Column(database.String(120), nullable=False)
    firstname = database.Column(database.String(80), nullable=False)
    lastname = database.Column(database.String(80), nullable=False)

class enrollment(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    student_name = database.Column(database.String(80), database.ForeignKey('student.firstname'))
    class_name = database.Column(database.String(80), database.ForeignKey('classes.Name'))
    grade = database.Column(database.Float)

class classes(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    Name = database.Column(database.String(80), unique=True, nullable=False)
    teacher_name = database.Column(database.String(80), nullable=False)
    teacher_id = database.Column(database.Integer, database.ForeignKey('teacher.id'))
    enrollment = database.relationship('enrollment', backref='Classes', lazy=True)
    capacity = database.Column(database.Integer)
    day = database.Column(database.String(80), nullable=False)
    time = database.Column(database.String(80), nullable=False)

class logoutButton(BaseView):
    @expose('/')
    def index(self):
        return redirect('/')

flaskAdmin = Admin(app)
flaskAdmin.add_view(ModelView(teacher, database.session))
flaskAdmin.add_view(ModelView(student, database.session))
flaskAdmin.add_view(ModelView(classes, database.session))
flaskAdmin.add_view(ModelView(enrollment, database.session))
flaskAdmin.add_view(logoutButton(name='Logout'))
 
with app.app_context():
    database.create_all()

@app.route('/')
def start_page():
    return render_template('login.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        studentName = student.query.filter_by(username=username).first()
        teacherName = teacher.query.filter_by(username=username).first()
        adminName = admin.query.filter_by(username=username).first()

        if studentName and studentName.password == password:
            return redirect(url_for('student_portal', username=username))
        elif teacherName and teacherName.password == password:
            return redirect(url_for('teacher_portal', username=username))
        elif adminName and adminName.password == password:
            return redirect(url_for('admin_portal', username=username))

    return redirect(url_for('start_page'))

@app.route('/student/<username>')
def student_portal(username):
    student_user = student.query.filter_by(username=username).first()
    if student_user:
        firstname = student_user.firstname
        lastname = student_user.lastname
        fullname = firstname + " " + lastname
        enrolled_classes = enrollment.query.filter_by(student_name=fullname).all()
        available_classes = classes.query.filter(classes.Name.notin_([en.class_name for en in enrolled_classes])).all()
        return render_template('student.html', username=username, firstname=firstname, lastname=lastname, fullname=fullname, available_classes=available_classes, enrolled_classes=enrolled_classes)
    else:
        # Handle the case when the username does not exist
        return "User not found"

@app.route('/teacher/<username>')
def teacher_portal(username):
    # Querying the teacher based on the provided username
    teacher_user = teacher.query.filter_by(username=username).first()
    
    if teacher_user:
        # Extracting first and last names from the teacher object
        first_name = teacher_user.firstname
        last_name = teacher_user.lastname
        
        # Filtering classes by teacher's first and last names
        teaching_classes = classes.query.filter_by(teacher_name=f"{first_name} {last_name}").all()
        
        return render_template('teacher.html', firstname=first_name, lastname=last_name, teaching_classes=teaching_classes)
    else:
        # Handle case where teacher with provided username is not found
        return "Teacher not found"

@app.route('/admin/<username>')
def admin_portal(username):
    user = admin.query.filter_by(username=username).first()
    firstname = user.firstname
    return redirect('http://localhost:5000/admin/')

@app.route('/create_acc.html')
def create_page():
    return render_template('create_acc.html')

@app.route('/create_acc', methods=['POST'])
def create_account():
    # Retrieve form data
    username = request.form['username']
    password = request.form['password']
    account_type = request.form['account_type']
    firstname = request.form['firstname']
    lastname = request.form['lastname']

    # Check if the username already exists
    existing_user = None
    if account_type == 'student':
        existing_user = student.query.filter_by(username=username).first()
    elif account_type == 'teacher':
        existing_user = teacher.query.filter_by(username=username).first()
    elif account_type == 'admin':
        existing_user = admin.query.filter_by(username=username).first()
    
    if existing_user:
        error_message = "Username already exists. Please choose a different username."
        return render_template('create_acc.html', error_message=error_message)

    # Create a new user account
    if account_type == 'student':
        new_user = student(username=username, password=password, firstname=firstname, lastname=lastname)
    elif account_type == 'teacher':
        new_user = teacher(username=username, password=password, firstname=firstname, lastname=lastname)
    elif account_type == 'admin':
        new_user = admin(username=username, password=password, firstname=firstname, lastname=lastname)
    # Add the new user to the database
    database.session.add(new_user)
    database.session.commit()
    return redirect(url_for('start_page'))

@app.route('/classes/' , methods = ['POST'])
def new_Class():
   submission = request.get_json()
   className = submission["class_name"]
   classTeacher = submission["class_teacher"]
   classSize = submission["class_size"]
   classID = submission["class_ID"]
   classDay = submission["class_day"]
   classTime = submission["class_time"]
   Nc = classes(id = classID, Name = className, teacher_name = classTeacher, capacity = classSize, day = classDay, time = classTime)
   database.session.add(Nc)
   database.session.commit()
   return jsonify({'message': 'Class created successfully'}), 201


@app.route('/enroll/<classname>/<firstname>/<lastname>', methods=['POST'])
def enroll_class(classname, firstname, lastname):
    # Concatenate first name and last name to get the full username
    username = firstname + " " + lastname
    
    existing_enrollment = enrollment.query.filter_by(student_name=username, class_name=classname).first()
    if existing_enrollment:
        # Student already exists in this class
        flash('You are already enrolled in {}!'.format(existing_enrollment.class_name))
        return redirect(url_for('student_portal', username=username))
    else:
        # adds the student enrolled into the DB
        length_enrollment = enrollment.query.filter_by(class_name=classname).count()
        class_capacity = classes.query.filter_by(Name=classname).first()
        if length_enrollment >= class_capacity.capacity:
            flash('Class {} is full!'.format(classname))
            return redirect(url_for('student_portal', username=username))
        else:
            class_to_enroll = enrollment(student_name=username, class_name=classname, grade=0)
            database.session.add(class_to_enroll)
            database.session.commit()
            # If everything works, refresh
            flash('You have successfully enrolled in {}!'.format(class_to_enroll.class_name))
            return redirect(url_for('student_portal', username=username))
        
@app.route('/drop/<classname>/<firstname>/<lastname>', methods=['DELETE'])
def drop_class(classname, firstname, lastname):
    fullname = firstname + " " + lastname
    class_to_drop = enrollment.query.filter_by(class_name=classname, student_name=fullname).first()
    if class_to_drop:
        database.session.delete(class_to_drop)
        database.session.commit()
        return jsonify({'message': 'Class dropped successfully'}), 200
    else:
        return jsonify({'error': 'Class not found'}), 404
    
@app.route('/enrolled_students/<class_name>')
def get_enrolled_students(class_name):
    enrolled_students = enrollment.query.filter_by(class_name=class_name).all()
    students_with_grades = [(enrollment.student_name, enrollment.grade) for enrollment in enrolled_students]
    return jsonify(students_with_grades)

@app.route('/edit_grade/<class_name>/<student_name>', methods=['POST'])
def edit_grade(class_name, student_name):
    try:
        # Retrieve the new grade from the request JSON data
        new_grade = request.json.get('newGrade')

        # Check if the new grade is provided
        if new_grade is None:
            return jsonify({'error': 'New grade not provided'}), 400

        # Find the enrollment record based on class name and student name
        enrollment_record = enrollment.query.filter_by(student_name=student_name, class_name=class_name).first()

        # Check if the enrollment record exists
        if enrollment_record:
            # Update the grade
            enrollment_record.grade = new_grade
            database.session.commit()
            return jsonify({'message': 'Grade updated successfully'}), 200
        else:
            return jsonify({'error': f'Enrollment record for {student_name} in {class_name} not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500




if __name__ == '__main__':
    app.run(debug=True)