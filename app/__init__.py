from flask import Flask
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
<<<<<<< HEAD
app.config.from_object(Config)
=======
app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = Config.SQLALCHEMY_TRACK_MODIFICATIONS
>>>>>>> b71daf771d8c14542199ecfa3d2fbd67ded55b68
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models
