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
)
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User

class UpdateAccountForm(FlaskForm):
    """Form for updating account details."""
    username = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    contact_info = StringField("Contact Info", validators=[Length(max=255)])  # Add this line
    submit = SubmitField('Update Account')
    address=StringField("Address",validators=[Length(max=255)])



class RegistrationForm(FlaskForm):
    """Form for new user registration."""
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=2, max=20)]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                "The username is taken. Please choose a different username."
            )

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
    location = StringField("Location", validators=[DataRequired()])  # Fixed typo from 'locations' to 'location'
    job_title = StringField("Job Title", validators=[DataRequired()])
    job_description = StringField("Job Description", validators=[DataRequired()])
    hourly_pay = StringField("Hourly Pay", validators=[DataRequired()])
    benefits = StringField("Benefits", validators=[DataRequired()])
    review = TextAreaField("Review", validators=[DataRequired()])
    rating = RadioField(
        "Rating",
        validators=[DataRequired()],
        choices=[('1', "1"), ('2', "2"), ('3', "3"), ('4', "4"), ('5', "5")],
    )
    recommendation = RadioField(
        "Recommendation",
        validators=[DataRequired()],
        choices=[(str(i), str(i)) for i in range(1, 11)],  # Fixed the line that got cut off
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
    resume= FileField("Upload Resume", validators=[DataRequired(), FileAllowed(['pdf', 'doc', 'docx'], 'Documents only!')])
    submit = SubmitField("Upload Resume")
