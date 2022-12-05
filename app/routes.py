from flask import render_template, request, redirect, flash, url_for
from app import app, db, bcrypt
from app.models import Reviews, Vacancies, User
from app.forms import RegistrationForm, LoginForm, ReviewForm
from flask_login import login_user, current_user, logout_user, login_required

app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

@app.route('/review/all')
def view_reviews():
    """An API for the user to view all the reviews entered"""
    entries = Reviews.query.all()
    return render_template('view_reviews.html', entries=entries)

@app.route('/review/new', methods=['GET', 'POST'])
@login_required
def new_review():
    form = ReviewForm()
    if form.validate_on_submit():
        review = Reviews(job_title=form.job_title.data, job_description=form.job_description.data, department=form.department.data, locations=form.locations.data,
                        hourly_pay=form.hourly_pay.data, benefits=form.benefits.data, review=form.review.data, rating=form.rating.data,
                        recommendation=form.recommendation.data, author=current_user)
        db.session.add(review)
        db.session.commit()
        flash('Review submitted successfully!', 'success')
        return redirect(url_for('view_reviews'))
    return render_template('create_review.html', title='New Review', form=form)


@app.route('/dashboard')
def getVacantJobs():
    """
        An API for the users to see all the available vacancies and their details
    """
    vacancies = Vacancies.query.all()
    return render_template('dashboard.html', vacancies=vacancies)

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
        return render_template('view_reviews.html', entries=entries)


@app.route('/')
@app.route('/home')
def home():
    """An API for the user to be able to access the homepage through the navbar"""
    entries = Reviews.query.all()
    return render_template('index.html', entries=entries)

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
        flash('Account created successfully! Please log in with your credentials.', 'success')
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
            flash('Login Unsuccessful. Please enter correct email and password.', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')

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
