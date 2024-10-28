from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    BooleanField,
    IntegerField,
    RadioField,
    TextAreaField,
    DecimalField
)
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User

class JobPostingForm(FlaskForm):
    jobTitle = StringField("Job Title", validators=[DataRequired(), Length(min=2, max=100)])
    jobDescription = TextAreaField("Job Description", validators=[DataRequired()])
    jobPayRate = DecimalField("Pay Rate", validators=[DataRequired()], places=2, rounding=None)
    jobLocation = StringField("Location", validators=[Length(max=100)])
    maxHoursAllowed = IntegerField("Maximum Working Hours Allowed")
    submit = SubmitField("Post Job")

class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    is_admin = BooleanField("Register as Admin")
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
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


class ReviewForm(FlaskForm):
    department = StringField("Department", validators=[DataRequired()])
    locations = StringField("Location", validators=[DataRequired()])
    job_title = StringField("Job Title", validators=[DataRequired()])
    job_description = StringField("Job Description", validators=[DataRequired()])
    hourly_pay = StringField("Hourly Pay", validators=[DataRequired()])
    benefits = StringField("Benefits", validators=[DataRequired()])
    review = TextAreaField("Review", validators=[DataRequired()])
    rating = RadioField(
        "Rating",
        validators=[DataRequired()],
        choices=[(1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")],
    )
    recommendation = RadioField(
        "Recommendation",
        validators=[DataRequired()],
        choices=[
            (1, "1"),
            (2, "2"),
            (3, "3"),
            (4, "4"),
            (5, "5"),
            (6, "6"),
            (7, "7"),
            (8, "8"),
            (9, "9"),
            (10, "10"),
        ],
    )
    submit = SubmitField("Submit your review")
