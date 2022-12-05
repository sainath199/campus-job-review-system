from flask import Flask
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager=LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
migrate = Migrate(app, db, render_as_batch=True)

@app.before_first_request
def create_table():
    db.create_all()

from app import routes, models