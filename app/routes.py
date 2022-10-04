from flask import render_template, request, redirect
from app import app, db
from app.models import Entry


@app.route('/')
@app.route('/index')
def index():
    entries = Entry.query.all()
    return render_template('index.html', entries=entries)


@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        form = request.form
        job_title = form.get('job_title')
        job_description = form.get('job_description')
        if not job_title or job_description:
            entry = Entry(job_title = job_title, job_description = job_description)
            db.session.add(entry)
            db.session.commit()
            return redirect('/')

