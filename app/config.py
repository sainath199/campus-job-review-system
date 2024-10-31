import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    """The class creates a connection to the database"""

    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Upload folder for resumes
    UPLOAD_FOLDER = os.path.join(basedir, 'app', 'static', 'resumes')



    # You might also want to set a maximum file size for uploads
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB

