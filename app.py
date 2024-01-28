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
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
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

class StandardCriteria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    criterion = db.Column(db.String(255))

def create_default_ratings(thesis):
    default_criteria = StandardCriteria.query.all()

    # Verknüpfen Sie die Standardbewertungskriterien mit der neuen Thesis
    for criterion in default_criteria:
        rating = ThesisRating(thesis=thesis, criterion=criterion.criterion, weight=0, rating=0)
        db.session.add(rating)

    db.session.commit()

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

@app.route('/about')
def about():
    return render_template('about_us.html')

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

    # Erzeugen Sie die Standardbewertungskriterien für die neue Thesis
    create_default_ratings(thesis)

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


@app.route('/thesis/<int:thesis_id>/update_ratings', methods=['POST'])
def update_ratings(thesis_id):
    thesis = Thesis.query.get(thesis_id)
    ratings = ThesisRating.query.filter_by(thesis_id=thesis_id).all()

    criteria = request.form.getlist('criterion[]')
    weights = request.form.getlist('weight[]')
    ratings_values = request.form.getlist('rating[]')

    # Aktualisieren der Bewertungskriterien
    for i in range(len(ratings)):
        ratings[i].criterion = criteria[i]
        ratings[i].weight = int(weights[i])
        ratings[i].rating = int(ratings_values[i])

    new_criterion = request.form['new_criterion']
    new_weight = request.form['new_weight']
    new_rating = request.form['new_rating']

    if new_criterion and new_weight and new_rating:
        # Hinzufügen neuer Bewertungskriterien

        new_rating_entry = ThesisRating(thesis=thesis, criterion=new_criterion, weight=int(new_weight), rating=int(new_rating))
        db.session.add(new_rating_entry)

    db.session.commit()

    return redirect(f'/thesis/{thesis_id}')


@app.route('/thesis/<int:thesis_id>/rating/delete/<int:rating_id>', methods=['GET', 'POST'])
def delete_rating(thesis_id, rating_id):
    thesis = Thesis.query.get(thesis_id)
    rating = ThesisRating.query.get(rating_id)

    if rating:
        db.session.delete(rating)
        db.session.commit()

    return redirect(f'/thesis/{thesis_id}')


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    # Lade die Liste der aktuellen Standardbewertungskriterien aus der Datenbank
    criteria = StandardCriteria.query.all()

    if request.method == 'POST':
        # Verarbeiten Sie das Formular zur Bearbeitung der Standardbewertungskriterien
        new_criterion = request.form['new_criterion']

        # Füge das neue Kriterium hinzu, wenn es nicht leer ist
        if new_criterion:
            standard_criterion = StandardCriteria(criterion=new_criterion)
            db.session.add(standard_criterion)
            db.session.commit()

            # Aktualisiere die Liste der Kriterien
            criteria = StandardCriteria.query.all()

    return render_template('settings.html', criteria=criteria)


@app.route('/settings/delete_criterion/<int:criterion_id>', methods=['GET', 'POST'])
def delete_criterion(criterion_id):
    criterion = StandardCriteria.query.get(criterion_id)

    if criterion:
        db.session.delete(criterion)
        db.session.commit()

    return redirect('/settings')


# =========================================================================

if __name__ == '__main__':
    app.run(debug=True)
