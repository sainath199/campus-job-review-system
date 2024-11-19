from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    BooleanField,
    IntegerField,
    RadioField,
    TextAreaField,
    FloatField
)
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from app.models import User


class UpdateAccountForm(FlaskForm):
    """Form for updating account details."""
    username = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    contact_info = StringField("Contact Info", validators=[Length(max=255)])
    address = StringField("Address", validators=[Length(max=255)])
    submit = SubmitField('Update Account')


class JobPostingForm(FlaskForm):
    """Form for posting a job."""
    jobTitle = StringField("Job Title", validators=[DataRequired(), Length(min=2, max=100)])
    jobDescription = TextAreaField("Job Description", validators=[DataRequired()])
    jobPayRate = FloatField("Pay Rate", validators=[DataRequired(), NumberRange(min=0, message="Pay rate must be a positive number.")])
    jobLocation = StringField("Location", validators=[Length(max=100)])
    maxHoursAllowed = IntegerField("Maximum Working Hours Allowed", validators=[DataRequired(), NumberRange(min=1, message="Hours must be at least 1.")])
    submit = SubmitField("Post Job")


class RegistrationForm(FlaskForm):
    """Form for user registration."""
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    is_admin = BooleanField("Register as Admin")
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("The username is taken. Please choose a different username.")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("An account already exists with this email address.")


class LoginForm(FlaskForm):
    """Form for user login."""
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


class ReviewForm(FlaskForm):
    """Form for submitting job reviews."""
    department = StringField("Department", validators=[DataRequired()])
    locations = StringField("Location", validators=[DataRequired()])
    job_title = StringField("Job Title", validators=[DataRequired()])
    job_description = StringField("Job Description", validators=[DataRequired()])
    hourly_pay = StringField("Hourly Pay", validators=[DataRequired()])
    benefits = StringField("Benefits", validators=[DataRequired()])
    review = TextAreaField("Review", validators=[DataRequired()])
    rating = RadioField(
        "Rating (1 is lowest, 5 is highest)",
        validators=[DataRequired()],
        choices=[("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5")],
    )
    recommendation = RadioField(
        "Recommendation (1 is lowest, 10 is highest)",
        validators=[DataRequired()],
        choices=[
            ("1", "1"),
            ("2", "2"),
            ("3", "3"),
            ("4", "4"),
            ("5", "5"),
            ("6", "6"),
            ("7", "7"),
            ("8", "8"),
            ("9", "9"),
            ("10", "10"),
        ],
    )
    submit = SubmitField("Submit your review")


class UserProfileForm(FlaskForm):
    """Form for updating user profile information."""
    name = StringField("Name", validators=[DataRequired(), Length(max=100)])
    contact_info = StringField("Contact Info", validators=[Length(max=255)])
    address = StringField("Address", validators=[Length(max=255)])
    submit = SubmitField("Update Profile")


class ResumeUploadForm(FlaskForm):
    """Form for uploading resumes."""
    resume = FileField("Upload Resume", validators=[DataRequired(), FileAllowed(['pdf', 'doc', 'docx'], 'Documents only!')])
    submit = SubmitField("Upload Resume")

