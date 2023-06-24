from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

students = []
theses = []


@app.route('/')
def index():
    return render_template('index.html', students=students, theses=theses)


@app.route('/add_student', methods=['POST'])
def add_student():
    student_name = request.form['name']
    students.append(student_name)
    return redirect(url_for('index'))


@app.route('/remove_student/<student_name>')
def remove_student(student_name):
    students.remove(student_name)
    return redirect(url_for('index'))


@app.route('/add_thesis', methods=['POST'])
def add_thesis():
    thesis_title = request.form['title']
    theses.append(thesis_title)
    return redirect(url_for('index'))


@app.route('/remove_thesis/<thesis_title>')
def remove_thesis(thesis_title):
    theses.remove(thesis_title)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
