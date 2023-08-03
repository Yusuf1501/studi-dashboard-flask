from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://user_version_2:pw_version_2@localhost/ba_version_2'  # Datenbankpfad
db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class Thesis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    student = db.relationship('Student', backref=db.backref('theses', lazy=True))

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    students = Student.query.all()
    return render_template('index.html', students=students)

@app.route('/add_student', methods=['POST'])
def add_student():
    student_name = request.form['name']
    new_student = Student(name=student_name)
    db.session.add(new_student)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/remove_student/<int:student_id>')
def remove_student(student_id):
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/add_thesis', methods=['POST'])
def add_thesis():
    thesis_title = request.form['title']
    student_id = int(request.form['student'])
    new_thesis = Thesis(title=thesis_title, student_id=student_id)
    db.session.add(new_thesis)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/remove_thesis/<int:thesis_id>')
def remove_thesis(thesis_id):
    thesis = Thesis.query.get_or_404(thesis_id)
    db.session.delete(thesis)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
