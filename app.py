from flask import Flask, render_template, request, redirect
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Konfiguration für die Verbindung zur MySQL-Datenbank
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://user_version_1:pw_version_1@localhost/ba_version_1'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Definition der Datenbankmodelle für Studenten und Abschlussarbeiten
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    matrikelnummer = db.Column(db.String(20))
    email = db.Column(db.String(255))


class Thesis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    student = db.relationship('Student', backref=db.backref('theses', lazy=True))
    ratings = db.relationship('ThesisRating', backref='thesis', lazy='dynamic')

class ThesisRating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    thesis_id = db.Column(db.Integer, db.ForeignKey('thesis.id'))
    criterion = db.Column(db.String(255))
    weight = db.Column(db.Integer)
    rating = db.Column(db.Integer)

# =====================================================================

@app.route('/')
def dashboard():
    students = Student.query.all()
    return render_template('dashboard.html', students=students)

@app.route('/search', methods=['GET'])
def search():
    search_term = request.args.get('search')
    students = Student.query.filter(Student.name.ilike(f'%{search_term}%')).all()
    return render_template('dashboard.html', students=students)

@app.route('/student/create', methods=['POST'])
def create_student():
    name = request.form['student_name']
    matrikelnummer = request.form['matrikelnummer']
    email = request.form['email']
    student = Student(name=name, matrikelnummer=matrikelnummer, email=email)
    db.session.add(student)
    db.session.commit()
    return redirect('/')

@app.route('/student/<int:student_id>')
def student_detail(student_id):
    student = Student.query.get(student_id)
    theses = Thesis.query.filter_by(student_id=student_id).all()
    return render_template('student_detail.html', student=student, theses=theses)

@app.route('/student/edit/<int:student_id>', methods=['POST'])
def edit_student(student_id):
    student = Student.query.get(student_id)
    student.name = request.form['name']
    student.matrikelnummer = request.form['matrikelnummer']
    student.email = request.form['email']
    db.session.commit()
    return redirect(f'/student/{student_id}')

@app.route('/student/delete/<int:student_id>')
def delete_student(student_id):
    student = Student.query.get(student_id)
    db.session.delete(student)
    db.session.commit()
    return redirect('/')

@app.route('/thesis/create', methods=['POST'])
def create_thesis():
    title = request.form['title']
    student_id = int(request.form['student_id'])
    student = Student.query.get(student_id)
    thesis = Thesis(title=title, student=student)
    db.session.add(thesis)
    db.session.commit()
    return redirect('/')

@app.route('/thesis/edit/<int:thesis_id>', methods=['POST'])
def edit_thesis(thesis_id):
    thesis = Thesis.query.get(thesis_id)
    thesis.title = request.form['title']
    thesis.student_id = request.form['student_id']
    db.session.commit()
    return redirect('/')

@app.route('/thesis/delete/<int:thesis_id>')
def delete_thesis(thesis_id):
    thesis = Thesis.query.get(thesis_id)
    db.session.delete(thesis)
    db.session.commit()
    return redirect('/')

@app.route('/thesis/<int:thesis_id>/add_rating', methods=['POST'])
def add_rating(thesis_id):
    thesis = Thesis.query.get(thesis_id)
    criterion = request.form['criterion']
    weight = int(request.form['weight'])
    rating = int(request.form['rating'])

    rating_entry = ThesisRating(thesis=thesis, criterion=criterion, weight=weight, rating=rating)
    db.session.add(rating_entry)
    db.session.commit()

    return redirect(f'/thesis/{thesis_id}')

@app.route('/thesis/<int:thesis_id>')
def thesis_detail(thesis_id):
    thesis = Thesis.query.get(thesis_id)
    ratings = ThesisRating.query.filter_by(thesis_id=thesis_id).all()
    total_weight = sum(rating.weight for rating in ratings)
    total_rating = sum(rating.rating * rating.weight for rating in ratings)
    average_rating = total_rating / total_weight if total_weight > 0 else 0

    return render_template(
        'thesis_detail.html',
        thesis=thesis,
        ratings=ratings,
        total_weight=total_weight,
        total_rating=total_rating,
        average_rating=average_rating
    )

@app.route('/thesis/<int:thesis_id>/rating/delete/<int:rating_id>', methods=['GET', 'POST'])
def delete_rating(thesis_id, rating_id):
    thesis = Thesis.query.get(thesis_id)
    rating = ThesisRating.query.get(rating_id)

    if rating:
        db.session.delete(rating)
        db.session.commit()

    return redirect(f'/thesis/{thesis_id}')

# =========================================================================

if __name__ == '__main__':
    app.run(debug=True)
