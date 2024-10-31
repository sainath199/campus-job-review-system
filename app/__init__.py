from flask import Flask
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os

# Initialize Flask app
app = Flask(__name__)

# Load configuration from config.py
app.config.from_object(Config)

# Print the upload folder path for debugging
print("Upload folder path:", app.config.get("UPLOAD_FOLDER"))

# Set up database and migration management
db = SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch=True)

# Set up password hashing
bcrypt = Bcrypt(app)

# Set up Flask-Login for user authentication
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"

# Create the database tables at the first request if they don't exist
@app.before_first_request
def create_table():
    db.create_all()

# Function to load a user from the database based on their user ID (for Flask-Login)
from app.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Import routes and models
from app import routes, models
