from flask import render_template, request, redirect, flash, url_for, abort
from app import app, db, bcrypt
from app.models import Reviews, Vacancies, User
from app.forms import RegistrationForm, LoginForm, ReviewForm, JobPostingForm, UpdateAccountForm, ResumeUploadForm
from flask_login import login_user, current_user, logout_user, login_required
from functools import wraps
from app.models import Notification
from app.utils import get_all_jobs_statistics, notify_users_about_new_job

from werkzeug.utils import secure_filename
import os



app.config["SECRET_KEY"] = "5791628bb0b13ce0c676dfde280ba245"
app.config["UPLOAD_FOLDER"] = "app/static/resumes"
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
@app.route("/home")
def home():
    """An API for the user to be able to access the homepage through the navbar"""
    entries = Reviews.query.all()
    return render_template("index.html", entries=entries)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            abort(403)  # Forbidden access
        return f(*args, **kwargs)
    return decorated_function

@app.route("/apply")
def apply():
    return redirect(url_for('job_listings'))

@app.route("/job_tracker")
def job_tracker():
    return render_template("job_tracker.html")


@app.route("/notifications/mark_read", methods=["POST"])
@login_required
def mark_notifications_read():
    notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).all()
    for notification in notifications:
        notification.is_read = True
    db.session.commit()
    flash("All notifications marked as read.", "success")
    return redirect(url_for("notifications"))

@app.route("/post_job_apply", methods=["GET", "POST"])
@login_required
def post_job_apply():
    if not current_user.is_admin:  # Check if the current user is not an admin
        return abort(403)
    form = JobPostingForm()
    if form.validate_on_submit():
        print("Form validated successfully.")
        new_job = Vacancies(
            jobTitle=form.jobTitle.data,
            jobDescription=form.jobDescription.data,
            jobLocation=form.jobLocation.data,
            jobPayRate=float(form.jobPayRate.data),
            maxHoursAllowed=form.maxHoursAllowed.data,
        )
        
        db.session.add(new_job)
        db.session.commit()
        flash(
            "Job posted successfully!", "success"
        )
        return redirect(url_for("job_listings_apply"))
    else:
        print("Form errors:",form.errors)
    return render_template("post_job.html", form=form)

@app.route("/post_job", methods=["GET", "POST"])
@login_required
def post_job():
    form = JobPostingForm()
    if request.method == "POST" and form.validate_on_submit():
        job_title = form.jobTitle.data
        job_description = form.jobDescription.data
        job_location = form.jobLocation.data
        pay_rate = float(form.jobPayRate.data)
        max_hours_allowed = form.maxHoursAllowed.data

        # Create the new job
        new_job = Vacancies(job_title, job_description, job_location, pay_rate, max_hours_allowed)
        db.session.add(new_job)
        db.session.commit()

        # Notify all users about the new job
        notify_users_about_new_job(job_title)

        flash("Job posted successfully and notifications created!", "success")
        return redirect(url_for("dashboard"))

    return render_template("post_job.html", form=form)

@app.route("/check_notifications", methods=["GET"])
@login_required
def check_notifications():
    unread_count = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()
    return {"unread_count": unread_count}, 200


@app.route("/notifications", methods=["GET", "POST"])
@login_required
def notifications():
    user_notifications = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.timestamp.desc()).all()
    # Mark all notifications as read
    for notification in user_notifications:
        notification.is_read = True
    db.session.commit()
    return render_template("notifications.html", notifications=user_notifications)


@app.context_processor
def inject_notifications_count():
    if current_user.is_authenticated:
        unread_notifications_count = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()
    else:
        unread_notifications_count = 0
    return dict(unread_notifications_count=unread_notifications_count)


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(
            username=form.username.data, 
            email=form.email.data, 
            password=hashed_password,
            is_admin=form.is_admin.data
        )
        db.session.add(user)
        db.session.commit()
        print("Registered user:", user.username, user.email)
        flash(
            "Account created successfully! Please log in with your credentials.",
            "success",
        )
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)

@app.route("/review/<int:review_id>/delete", methods=["POST"])
@login_required
def delete_review(review_id):
    review = Reviews.query.get_or_404(review_id)

    if review.user_id == current_user.id or current_user.is_admin:    
        db.session.delete(review)
        db.session.commit()
        flash("The review has been deleted!", "success")
        return redirect(url_for("view_reviews"))
    else:
        flash('You cannot delete this review. It was not created by you.', 'danger')
        return redirect(url_for('view_reviews'))

@app.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if not current_user.is_admin:
        return "You do not have permission to delete this user", 403
    db.session.delete(user)
    db.session.commit()
    flash('User has been deleted successfully.', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/toggle_admin/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def toggle_admin(user_id):
    user = User.query.get_or_404(user_id)
    if not current_user.is_admin:
        abort(403) 
    user.is_admin = not user.is_admin
    db.session.commit()
    flash('User admin status has been updated.', 'success')
    return redirect(url_for('admin_dashboard')) 

@app.route("/admin/dashboard")
@login_required
@admin_required
def admin_dashboard():
    if not current_user.is_admin:  # Assuming you have an is_admin attribute
        abort(403)
    reviews = Reviews.query.all()
    users = User.query.all()
    jobs = Vacancies.query.all() 
    return render_template('admin_dashboard.html', reviews=reviews, users=users, jobs=jobs)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("home"))
        else:
            flash(
                "Login Unsuccessful. Please enter correct email and password.", "danger"
            )
    return render_template("login.html", title="Login", form=form)


@app.route("/logout", methods=["GET", "POST"])
def logout():
    logout_user()
    flash("Logged out successfully!", "success")
    return redirect(url_for("home"))


@app.route("/review/all")
def view_reviews():
    """An API for the user to view all the reviews entered"""
    entries = Reviews.query.all()
    return render_template("view_reviews.html", entries=entries)


@app.route("/account", methods=["GET", "POST"])
@login_required
def profile():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.contact_info = form.contact_info.data
        current_user.address = form.address.data
        
        if 'resume' in request.files:
            file = request.files['resume']
            if file and allowed_file(file.filename):
                if not os.path.exists(app.config["UPLOAD_FOLDER"]):
                    os.makedirs(app.config["UPLOAD_FOLDER"])

                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                file.save(file_path)

                # Save the file path in the user model
                current_user.resume_file_path = file_path  # Ensure this field exists in your User model

        db.session.commit()
        flash("Your account has been updated!", "success")
        return redirect(url_for("profile"))  # Redirect to the profile page to show changes
    elif request.method == "GET":
        # Populate the form fields with current user data
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.contact_info.data = current_user.contact_info
        form.address.data = current_user.address

    # Generate the URL for the resume
    resume_url = url_for('static', filename='resumes/' + os.path.basename(current_user.resume_file_path)) if current_user.resume_file_path else None
    return render_template("account.html", title="Account", form=form, resume_url=resume_url)

@app.route("/feedback", methods=['GET', 'POST'])
@login_required
def feedback():
    if request.method == 'POST':
        feedback_content = request.form.get('feedback')
        # You can save this feedback to the database or process it as needed
        flash("Thank you for your feedback!", "success")
        return redirect(url_for('feedback'))
    return render_template('feedback.html')

@app.route("/upload_resume", methods=["GET", "POST"])
@login_required
def upload_resume():
    form = ResumeUploadForm()
    if form.validate_on_submit():
        if 'resume' in request.files:
            file = request.files['resume']
            if file and allowed_file(file.filename):
                # Ensure the upload directory exists
                if not os.path.exists(app.config["UPLOAD_FOLDER"]):
                    os.makedirs(app.config["UPLOAD_FOLDER"])

                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                file.save(file_path)
                current_user.resume_file_path = file_path  # Assuming this is how you track the resume
                db.session.commit()
                flash("Resume uploaded successfully!", "success")
                return redirect(url_for("profile"))
            else:
                flash("Invalid file type. Please upload a PDF or Word document.", "danger")
    return render_template("upload_resume.html", title="Upload Resume", form=form)
                           
@app.route('/delete-job/<int:job_id>', methods=['POST'])
@login_required
@admin_required
def delete_job(job_id):
    # Fetch and delete the job based on job_id
    job = Vacancies.query.get_or_404(job_id)
    if not current_user.is_admin:  # Check if the current user is not an admin
        return abort(403)
    if job:
        db.session.delete(job)
        db.session.commit()
        flash("Job deleted successfully!", "success")
    else:
        flash("Job not found.", "danger")
    return redirect(url_for('getVacantJobs'))

@app.route("/review/new", methods=["GET", "POST"])
@login_required
def new_review():
    form = ReviewForm()
    if form.validate_on_submit():
        review = Reviews(
            job_title=form.job_title.data,
            job_description=form.job_description.data,
            department=form.department.data,
            locations=form.locations.data,
            hourly_pay=form.hourly_pay.data,
            benefits=form.benefits.data,
            review=form.review.data,
            rating=form.rating.data,
            recommendation=form.recommendation.data,
            author=current_user,
        )
        db.session.add(review)
        db.session.commit()
        flash("Review submitted successfully!", "success")
        return redirect(url_for("view_reviews"))
    return render_template(
        "create_review.html", title="New Review", form=form, legend="Add your Review"
    )


@app.route("/review/<int:review_id>")
def review(review_id):
    review = Reviews.query.get_or_404(review_id)
    return render_template("review.html", review=review)


@app.route("/review/<int:review_id>/update", methods=["GET", "POST"])
@login_required
def update_review(review_id):
    review = Reviews.query.get_or_404(review_id)
    if review.author != current_user:
        abort(403)
    form = ReviewForm()
    if form.validate_on_submit():
        review.job_title = form.job_title.data
        review.job_description = form.job_description.data
        review.department = form.department.data
        review.locations = form.locations.data
        review.hourly_pay = form.hourly_pay.data
        review.benefits = form.benefits.data
        review.review = form.review.data
        review.rating = form.rating.data
        review.recommendation = form.recommendation.data
        db.session.commit()
        flash("Your review has been updated!", "success")
        return redirect(url_for("view_reviews"))
    elif request.method == "GET":
        form.job_title.data = review.job_title
        form.job_description.data = review.job_description
        form.department.data = review.department
        form.locations.data = review.locations
        form.hourly_pay.data = review.hourly_pay
        form.benefits.data = review.benefits
        form.review.data = review.review
        form.rating.data = review.rating
        form.recommendation.data = review.recommendation
    return render_template(
        "create_review.html", title="Update Review", form=form, legend="Update Review"
    )

@app.route("/dashboard")
@login_required
def dashboard():
    job_statistics = get_all_jobs_statistics()
    return render_template('dashboard.html', job_statistics=job_statistics)


@app.route("/job_listings", methods=['GET'])
def job_listings():
    search_title = request.args.get('search', '').strip()  # Get the job title search query
    job_location = request.args.get('jobLocation', '').strip()  # Get the job location
    pay_rate = request.args.get('payRate', '').strip()  # Get the selected pay rate
    max_hours_allowed = request.args.get('maxHoursAllowed', '').strip()  # Get max hours allowed
    
    query = Vacancies.query

    # Apply filters based on the search criteria
    if search_title:
        query = query.filter(Vacancies.jobTitle.ilike(f'%{search_title}%'))
    
    if job_location:
        query = query.filter(Vacancies.jobLocation.ilike(f'%{job_location}%'))

    if pay_rate:
        if pay_rate == "30+":
            query = query.filter(Vacancies.jobPayRate > 30)
        else:
            query = query.filter(Vacancies.jobPayRate <= float(pay_rate))

    if max_hours_allowed:
        if max_hours_allowed == "40+":
            query = query.filter(Vacancies.maxHoursAllowed > 40)
        else:
            query = query.filter(Vacancies.maxHoursAllowed <= int(max_hours_allowed))
    
    vacancies = query.all()  # Execute the query
    
    return render_template("dashboard.html", vacancies=vacancies)

applied_jobs = []  # Temporary in-memory storage for applied jobs

@app.route('/apply/<int:job_id>', methods=['POST'])
@login_required
def apply_job(job_id):
    job = Vacancies.query.get_or_404(job_id)
    if not any(applied_job['id'] == job_id for applied_job in applied_jobs):
        applied_jobs.append({
            'id': job.vacancyId,
            'title': job.jobTitle,
            'location': job.jobLocation,
            'pay_rate': job.jobPayRate,
            'user_id': current_user.id,
            'status': 'Initiated'  # Initial status
        })
        flash(f"You have applied for {job.jobTitle}.", "success")
    else:
        flash(f"You already applied for {job.jobTitle}.", "info")
    return redirect(url_for('job_listings'))

@app.route('/applied_jobs')
@login_required
def applied_jobs_list():
    user_applied_jobs = [job for job in applied_jobs if job['user_id'] == current_user.id]
    return render_template('applied_jobs.html', applied_jobs=user_applied_jobs)

@app.route('/cancel_application/<int:job_id>', methods=['POST'])
@login_required
def cancel_application(job_id):
    global applied_jobs
    applied_jobs = [job for job in applied_jobs if not (job['id'] == job_id and job['user_id'] == current_user.id)]
    flash("Application canceled successfully.", "success")
    return redirect(url_for('applied_jobs_list'))

@app.route('/show_applicants/<int:job_id>', methods=['GET'])
@login_required
@admin_required
def show_applicants(job_id):
    applicants = [job for job in applied_jobs if job['id'] == job_id]
    job = Vacancies.query.get_or_404(job_id)
    return render_template('show_applicants.html', applicants=applicants, job=job)

@app.route('/approve_application/<int:job_id>/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def approve_application(job_id, user_id):
    global applied_jobs
    for job in applied_jobs:
        if job['id'] == job_id and job['user_id'] == user_id:
            job['status'] = 'Approved'  # Update status
            flash(f"Application for job ID {job_id} approved.", "success")
            break
    return redirect(url_for('show_applicants', job_id=job_id))

@app.route('/reject_application/<int:job_id>/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def reject_application(job_id, user_id):
    global applied_jobs
    for job in applied_jobs:
        if job['id'] == job_id and job['user_id'] == user_id:
            job['status'] = 'Rejected'  # Update status instead of removing
            flash(f"Application for job ID {job_id} rejected.", "danger")
            break
    return redirect(url_for('show_applicants', job_id=job_id))
