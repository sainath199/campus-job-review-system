from flask import render_template, request, redirect,flash, url_for
from app import app, db, bcrypt
from app.models import Reviews, Vacancies,User
from app.forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import login_user,current_user,logout_user

app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
@app.route('/review')
def review():
    """
    An API for the user review page, which helps the user to add reviews
    """
    entries = Reviews.query.all()
    return render_template('review-page.html', entries=entries)


@app.route('/dashboard')
def getVacantJobs():
    """
        An API for the users to see all the available vacancies and their details
    """
    vacancies = Vacancies.query.all()
    return render_template('dashboard.html', vacancies=vacancies)


@app.route('/pageContent')
def page_content():
    """An API for the user to view all the reviews entered"""
    entries = Reviews.query.all()
    return render_template('page_content.html', entries=entries)


@app.route('/pageContentPost', methods=['POST'])
def page_content_post():
    """An API for the user to view specific reviews depending on the job title"""
    if request.method == 'POST':
        form = request.form
        search_title = form.get('search')
        if search_title.strip() == '':
            entries = Reviews.query.all()
        else:
            entries = Reviews.query.filter_by(job_title=search_title)
        return render_template('page_content.html', entries=entries)


@app.route('/')
@app.route('/home')
def home():
    """An API for the user to be able to access the homepage through the navbar"""
    entries = Reviews.query.all()
    return render_template('index.html', entries=entries)


@app.route('/add', methods=['POST'])
def add():
    """An API to help users add their reviews and store it in the database"""
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
        recommendation = form.get('recommendation')

        entry = Reviews(job_title=title, job_description=description, department=department, locations=locations,
                        hourly_pay=hourly_pay, benefits=benefits, review=review, rating=rating,
                        recommendation=recommendation)
        db.session.add(entry)
        db.session.commit()
        return redirect('/')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
         return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))
# @app.route('/update/<int:id>')
# def updateRoute(id):
#     if not id or id != 0:
#         entry = Reviews.query.get(id)
#         if entry:
#             return render_template('update.html', entry=entry)
#
#
# @app.route('/update/<int:id>', methods=['POST'])
# def update(id):
#     if not id or id != 0:
#         entry = Reviews.query.get(id)
#         if entry:
#             form = request.form
#             title = form.get('job_title')
#             description = form.get('job_description')
#             department = form.get('department')
#             locations = form.get('locations')
#             hourly_pay = form.get('hourly_pay')
#             benefits = form.get('benefits')
#             review = form.get('review')
#             rating = form.get('rating')
#             entry.title = title
#             entry.description = description
#             entry.department = department
#             entry.locations = locations
#             entry.hourly_pay = hourly_pay
#             entry.benefits = benefits
#             entry.review = review
#             entry.rating = rating
#             db.session.commit()
#         return redirect('/')
#
#
# @app.route('/delete/<int:id>')
# def delete(id):
#     if not id or id != 0:
#         entry = Reviews.query.get(id)
#         if entry:
#             db.session.delete(entry)
#             db.session.commit()
#         return redirect('/')
