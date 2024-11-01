import os
import sys
import pytest
from io import BytesIO
from app import db, app  # Directly import the app instance
from app.models import User 
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

sys.path.append(os.getcwd()[:-5]+"app")
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # Add parent folder to path

def test_index_route():
    response = app.test_client().get('/')
    assert response.status_code == 200

def test_index_route_2():
    response = app.test_client().get('/home')
    assert response.status_code == 200

def test_register_get():
    response = app.test_client().get('/register')
    assert response.status_code == 200

def test_register_post():
    response = app.test_client().post('/register', data={ 'username': 'asavla2', 'password': 'pass', 'email': 'asavla2@ncsu.edu'  })
    assert response.status_code == 200

def test_login_get():
    response = app.test_client().get('/login')
    assert response.status_code == 200

def test_login_post():
    response = app.test_client().post('/login', data={'email': 'asavla2@ncsu.edu', 'password': 'pass'  })
    assert response.status_code == 200

def test_logout_get():
    response = app.test_client().get('/logout')
    assert response.status_code == 302

def test_view_review_all():
    response = app.test_client().get('/review/all')
    assert response.status_code == 200

def test_add_review_route_get():
    response = app.test_client().get('/review/new')
    assert response.status_code == 302

def test_add_review_route_post():
    response = app.test_client().post('/review/new', data=
    {"job_title":"1",
    "job_description":"2",
    "department":"3",
    "locations":"4",
    "hourly_pay":"5",
    "benefits":"6",
    "review":"7",
    "rating":"2",
    "recommendation":"2",
    })
    assert response.status_code == 302

def test_view_review():
    response1 = app.test_client().get('/review/5')
    response2 = app.test_client().get('/review/1')
    assert response1.status_code == 200
    assert response2.status_code == 404

def test_update_review():
    response1 = app.test_client().post('/review/5',  data=
    {"job_title":"1",
    "job_description":"2",
    "department":"3",
    "locations":"4",
    "hourly_pay":"5",
    "benefits":"6",
    "review":"7",
    "rating":"2",
    "recommendation":"2",
    })
    assert response1.status_code == 405

# def test_page_content_route():
#     response = app.test_client().post('/pageContentPost',data={"search":"Setup"})
#     assert response.status_code == 200

# def test_add_post_route():
#     response = app.test_client().post('/pageContentPost',data=
#     {"job_title":"1",
#     "job_description":"2",
#     "department":"3",
#     "locations":"4",
#     "hourly_pay":"5",
#     "benefits":"6",
#     "review":"7",
#     "rating":"2",
#     "recommendation":"2",
#     })
#     assert response.status_code == 200

    

# def test_review_route():
#     response = app.test_client().get('/pageContent')
#     assert response.status_code == 200

def test_dashboard_route():
    response = app.test_client().get('/dashboard')
    assert response.status_code == 200

def test_account_route():
    response = app.test_client().get('/account')
    assert response.status_code == 302

@pytest.fixture
def authenticated_client():
    app.config['TESTING'] = True  # Set the testing mode
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use an in-memory database for tests

    with app.app_context():
        db.create_all()  # Create the database schema
        # Create a test user and authenticate
        user = User(username='testuser', password='password', email='test@example.com')  # Adjust according to your model
        db.session.add(user)
        db.session.commit()

        # Log in the user here if your application requires authentication
        with app.test_client() as client:
            client.post('/login', data={'username': 'testuser', 'password': 'password'})
            yield client  # This provides the test client to your test case

        db.session.remove()
        db.drop_all()  # Clean up the database after tests



# 1. Test updating account with valid data
def test_update_account_valid(authenticated_client):
    response = authenticated_client.post('/account', data={
        'username': 'updateduser',
        'email': 'updatedemail@example.com',
        'contact_info': '1234567890',
        'address': '123 New Street'
    })
    assert response.status_code == 302  # Redirect after update



    
# 2. Test uploading resume with valid PDF file
def test_resume_upload_valid_pdf(authenticated_client):
    data = {
        'file': (BytesIO(b'PDF content'), 'resume.pdf')  # Match the form field
    }
    response = authenticated_client.post('/upload_resume', content_type='multipart/form-data', data=data)
    assert response.status_code == 302  # Redirect after successful upload

# 3. Test uploading resume with valid DOC file
def test_resume_upload_valid_doc(authenticated_client):
    data = {
        'file': (BytesIO(b'DOC content'), 'resume.doc')  # Match the form field
    }
    response = authenticated_client.post('/upload_resume', content_type='multipart/form-data', data=data)
    assert response.status_code == 302  # Redirect after successful upload

# 4. Test updating account with empty contact info
def test_update_account_empty_contact(authenticated_client):
    response = authenticated_client.post('/account', data={
        'username': 'testuser',
        'email': 'user@example.com',
        'contact_info': '',
        'address': '123 Main Street'
    })
    assert response.status_code == 302



# 5. Test account update with an address containing special characters
def test_update_account_special_characters_address(authenticated_client):
    response = authenticated_client.post('/account', data={
        'username': 'testuser',
        'email': 'user@example.com',
        'contact_info': '1234567890',
        'address': '!@#%^&*()_+<>?'
    })
    assert response.status_code == 302


# 6. Test updating account with contact info containing special characters
def test_update_account_special_characters_contact(authenticated_client):
    response = authenticated_client.post('/account', data={
        'username': 'testuser',
        'email': 'user@example.com',
        'contact_info': '+1-(800)-555-0123',
        'address': '123 Main Street'
    })
    assert response.status_code == 302

# 7. Test uploading a resume with a valid .docx file type
def test_resume_upload_valid_docx(authenticated_client):
    data = {
        'file': (BytesIO(b'DOCX content'), 'resume.docx')  # Match the form field
    }
    response = authenticated_client.post('/upload_resume', content_type='multipart/form-data', data=data)
    assert response.status_code == 302  # Redirect after successful upload


