from flask import render_template, request, redirect
from app import app, db
from app.models import Reviews


@app.route('/review')
def review():
    entries = Reviews.query.all()
    return render_template('review-page.html', entries=entries)


@app.route('/pageContent')
def page_content():
        entries = Reviews.query.all()
        return render_template('page_content.html', entries=entries)

@app.route('/pageContentPost', methods=['POST'])
def page_content_post():
        print("hi")
        if request.method == 'POST':
            form = request.form
            search_title = form.get('search')
            entries = Reviews.query.filter_by(job_title=search_title)
            return render_template('page_content.html', entries=entries)

@app.route('/')
@app.route('/home')
def home():
    entries = Reviews.query.all()
    return render_template('index.html', entries=entries)


@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        form = request.form
        title = form.get('job_title')
        description = form.get('job_description')
        department = form.get('department')
        locations = form.get('locations')
        hourly_pay = form.get('hourly_pay')
        benefits = form.get('benefits')
        review = form.get('review')
        rating = form.get('rating')

        entry = Reviews(job_title = title, job_description = description, department = department, locations = locations, hourly_pay = hourly_pay, benefits = benefits, review=review, rating=rating)
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
            department = form.get('department')
            locations = form.get('locations')
            hourly_pay = form.get('hourly_pay')
            benefits = form.get('benefits')
            review = form.get('review')
            rating = form.get('rating')
            entry.title = title
            entry.description = description
            entry.department = department
            entry.locations = locations
            entry.hourly_pay = hourly_pay
            entry.benefits = benefits
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
