from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Beispiel-Daten für Studenten und Abschlussarbeiten
students = [
    {"id": 1, "name": "Max Mustermann"},
    {"id": 2, "name": "Erika Musterfrau"}
]

theses = [
    {"id": 1, "title": "Thesis 1", "student_id": 1},
    {"id": 2, "title": "Thesis 2", "student_id": 2}
]


@app.route('/')
def dashboard():
    return render_template('dashboard.html', students=students, theses=theses)


@app.route('/student/create', methods=['POST'])
def create_student():
    name = request.form['name']
    student_id = len(students) + 1
    students.append({"id": student_id, "name": name})
    return redirect('/')


@app.route('/student/edit/<int:student_id>', methods=['POST'])
def edit_student(student_id):
    name = request.form['name']
    for student in students:
        if student['id'] == student_id:
            student['name'] = name
            break
    return redirect('/')


@app.route('/student/delete/<int:student_id>')
def delete_student(student_id):
    for student in students:
        if student['id'] == student_id:
            students.remove(student)
            break
    return redirect('/')


@app.route('/thesis/create', methods=['POST'])
def create_thesis():
    title = request.form['title']
    student_id = int(request.form['student_id'])
    thesis_id = len(theses) + 1
    theses.append({"id": thesis_id, "title": title, "student_id": student_id})
    return redirect('/')


@app.route('/thesis/edit/<int:thesis_id>', methods=['POST'])
def edit_thesis(thesis_id):
    title = request.form['title']
    for thesis in theses:
        if thesis['id'] == thesis_id:
            thesis['title'] = title
            break
    return redirect('/')


@app.route('/thesis/delete/<int:thesis_id>')
def delete_thesis(thesis_id):
    for thesis in theses:
        if thesis['id'] == thesis_id:
            theses.remove(thesis)
            break
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
