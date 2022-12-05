from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Vacancies(db.Model):

    """Model which stores the information of the reviews submitted"""
    vacancyId = db.Column(db.Integer, primary_key=True)
    jobTitle = db.Column(db.String(500), index=True, nullable=False)
    jobDescription = db.Column(db.String(1000), index=True, nullable=False)
    jobLocation = db.Column(db.String(500), index=True, nullable=False)
    jobPayRate = db.Column(db.String(120), index=True, nullable=False)
    maxHoursAllowed = db.Column(db.Integer, nullable=False)

    def __init__(self, jobTitle, jobDescription, jobLocation, jobPayRate, maxHoursAllowed):
        self.jobTitle = jobTitle
        self.jobDescription = jobDescription
        self.jobLocation = jobLocation
        self.jobPayRate = jobPayRate
        self.maxHoursAllowed = maxHoursAllowed


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')