from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    is_read = db.Column(db.Boolean, default=False)  # Track if the notification has been read
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class Reviews(db.Model):
    """Model which stores the information of the reviews submitted"""

    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String(64), index=True, nullable=False)
    locations = db.Column(db.String(120), index=True, nullable=False)
    job_title = db.Column(db.String(64), index=True, nullable=False)
    job_description = db.Column(db.String(120), index=True, nullable=False)
    hourly_pay = db.Column(db.String(10), nullable=False)
    benefits = db.Column(db.String(120), index=True, nullable=False)
    review = db.Column(db.String(120), index=True, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    recommendation = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

class UserProfile(db.Model):
    """Model which stores additional profile information for users"""

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    contact_info = db.Column(db.String(255), nullable=True)
    address = db.Column(db.String(255), nullable=True)


class Vacancies(db.Model):

    """Model which stores the information of the reviews submitted"""
    # id = db.Column(db.Integer, primary_key=True)  # Primary key
    vacancyId = db.Column(db.Integer, primary_key=True)
    jobTitle = db.Column(db.String(500), index=True, nullable=False)
    jobDescription = db.Column(db.String(1000), index=True, nullable=False)
    jobLocation = db.Column(db.String(500), index=True, nullable=False)
    jobPayRate = db.Column(db.String(120), index=True, nullable=False)
    maxHoursAllowed = db.Column(db.Integer, nullable=False)

    def __init__(
        self, jobTitle, jobDescription, jobLocation, jobPayRate, maxHoursAllowed
    ):
        self.jobTitle = jobTitle
        self.jobDescription = jobDescription
        self.jobLocation = jobLocation
        self.jobPayRate = jobPayRate
        self.maxHoursAllowed = maxHoursAllowed



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default.jpg")
    contact_info = db.Column(db.String(255), nullable=True)
    address = db.Column(db.String(255), nullable=True)
    resumes = db.relationship("Resume", backref="user", lazy=True)
    resume_file_path = db.Column(db.String(300), nullable=True)
    password = db.Column(db.String(60), nullable=False)
    reviews = db.relationship("Reviews", backref="author", lazy=True)
    is_admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Resume(db.Model):
    """Model which stores information about uploaded resumes"""

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    resume_file = db.Column(db.String(255), nullable=False)  # Path to uploaded resume file
    upload_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def _repr_(self):
        return f"Resume(User ID: '{self.user_id}', File: '{self.resume_file}', Uploaded: '{self.upload_date}')"
