import os
basedir = os.path.abspath(os.path.dirname(__file__))

<<<<<<< HEAD
class Config(object):
    # SECRET_KEY = 'do-or-do-not-there-is-no-try'
=======
class Config():
>>>>>>> b71daf771d8c14542199ecfa3d2fbd67ded55b68
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False