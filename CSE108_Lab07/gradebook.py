from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///grades.sqlite3'
db = SQLAlchemy(app)

class Grade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(100), nullable=False)
    grade = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"Grade(name='{self.student_name}', grade={self.grade})"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/grades/<name>', methods=['GET'])
def get_grade(name):
    grade = Grade.query.filter_by(student_name=name).first()
    if grade:
        return jsonify({grade.student_name, grade.grade})
    else:
        return jsonify({'message': 'Student not found'}), 404

@app.route('/grades', methods=['GET'])
def get_all_grades():
    all_grades = Grade.query.all()
    grade_list = [{'student_name': grade.student_name, 'grade': grade.grade} for grade in all_grades]
    return jsonify(grade_list)

@app.route('/grades/addStudent', methods=['POST'])
def create_grade():
    data = request.get_json()
    name = data.get('name')
    grade = data.get('grade')
    new_grade = Grade(student_name=name, grade=grade)
    db.session.add(new_grade)
    db.session.commit()
    return jsonify({'message': 'Grade created successfully'}), 201

@app.route('/grades/editStudent/<name>', methods=['PUT'])
def edit_grade(name):
    grade = Grade.query.filter_by(student_name=name).first()
    if not grade:
        return jsonify({'message': 'Student not found'}), 404
    data = request.get_json()
    grade.grade = data.get('grade')
    db.session.commit()
    return jsonify({'message': 'Grade updated successfully'})

@app.route('/grades/deleteStudent/<name>', methods=['DELETE'])
def delete_grade(name):
    grade = Grade.query.filter_by(student_name=name).first()
    if not grade:
        return jsonify({'message': 'Student not found'}), 404
    db.session.delete(grade)
    db.session.commit()
    return jsonify({'message': 'Grade deleted successfully'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
