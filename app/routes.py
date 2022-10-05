from flask import render_template, request, redirect
from app import app, db
<<<<<<< HEAD
from app.models import Reviews
=======
from app.models import Entry
>>>>>>> b71daf771d8c14542199ecfa3d2fbd67ded55b68


@app.route('/')
@app.route('/index')
def index():
<<<<<<< HEAD
    entries = Reviews.query.all()
=======
    entries = Entry.query.all()
>>>>>>> b71daf771d8c14542199ecfa3d2fbd67ded55b68
    return render_template('index.html', entries=entries)


@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        form = request.form
<<<<<<< HEAD
        title = form.get('job_title')
        description = form.get('job_description')
        review = form.get('review')
        rating = form.get('rating')
        entry = Reviews(job_title = title, job_description = description, review=review, rating=rating)
        db.session.add(entry)
        db.session.commit()
        return redirect('/')


@app.route('/update/<int:id>')
def updateRoute(id):
    if not id or id != 0:
        entry = Reviews.query.get(id)
        if entry:
            return render_template('update.html', entry=entry)


@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    if not id or id != 0:
        entry = Reviews.query.get(id)
        if entry:
            form = request.form
            title = form.get('job_title')
            description = form.get('job_description')
            review = form.get('review')
            rating = form.get('rating')
            entry.title = title
            entry.description = description
            entry.review = review
            entry.rating = rating
            db.session.commit()
        return redirect('/')


@app.route('/delete/<int:id>')
def delete(id):
    if not id or id != 0:
        entry = Reviews.query.get(id)
        if entry:
            db.session.delete(entry)
            db.session.commit()
        return redirect('/')
=======
        job_title = form.get('job_title')
        job_description = form.get('job_description')
        if not job_title or job_description:
            entry = Entry(job_title = job_title, job_description = job_description)
            db.session.add(entry)
            db.session.commit()
            return redirect('/')

>>>>>>> b71daf771d8c14542199ecfa3d2fbd67ded55b68
