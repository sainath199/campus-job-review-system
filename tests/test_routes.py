import os
import sys
import pytest
import io
from io import BytesIO
from app import db, app  # Directly import the app instance
from app.models import User 
import warnings
from werkzeug.security import check_password_hash
from app.models import UserProfile, Resume
warnings.filterwarnings("ignore", category=DeprecationWarning)
from flask import get_flashed_messages


sys.path.append(os.getcwd()[:-5]+"app")

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


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # Add parent folder to path
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

# 8. Test uploading a resume with a non-PDF/DOC/DOCX file type
def test_resume_upload_invalid_file_type(authenticated_client):
    data = {
        'resume': (BytesIO(b'Image content'), 'resume.png')  # Invalid file type
    }
    response = authenticated_client.post('/upload_resume', content_type='multipart/form-data', data=data)
    assert response.status_code == 200  # Expect a 200 due to validation error, check for flash message.
    assert b'Invalid file type. Please upload a PDF or Word document.' in response.data

# 9. Test uploading a blank resume file
def test_resume_upload_blank_file(authenticated_client):
    data = {
        'resume': (BytesIO(b''), 'resume.pdf')  # Empty file
    }
    response = authenticated_client.post('/upload_resume', content_type='multipart/form-data', data=data)
    assert response.status_code == 200  # Also expect a 200 due to validation error, check for flash message.
    assert b'Invalid file type. Please upload a PDF or Word document.' in response.data

# 10. Test uploading a resume with a duplicate file name
def test_resume_upload_duplicate_filename(authenticated_client):
    # First upload a valid file
    first_upload = {
        'resume': (BytesIO(b'Content'), 'resume.pdf')
    }
    authenticated_client.post('/upload_resume', content_type='multipart/form-data', data=first_upload)
    
    # Attempt to upload a second file with the same name
    second_upload = {
        'resume': (BytesIO(b'Content for second upload'), 'resume.pdf')  # Duplicate name
    }
    
    response = authenticated_client.post('/upload_resume', content_type='multipart/form-data', data=second_upload)
    assert response.status_code == 200  # Expect the proper flash message for duplicate filename.
    assert b'Invalid file type. Please upload a PDF or Word document.' in response.data

# 11. Test updating account information without a resume upload
def test_update_account_without_resume_upload(authenticated_client):
    response = authenticated_client.post('/account', data={
        'username': 'updateduser',
        'email': 'updatedemail@example.com',
        'contact_info': '1234567890',
        'address': '123 New Street'
    })
    assert response.status_code == 302  # Redirect after update

# 12. Test updating account email to an existing user’s email
def test_update_account_email_already_exists(authenticated_client):
    existing_user = User(username='existinguser', password='password', email='existing@example.com')
    db.session.add(existing_user)
    db.session.commit()
    
    response = authenticated_client.post('/account', data={
        'username': 'updateduser',
        'email': 'email@gmail.com',  # existing email
        'contact_info': '1234567890',
        'address': '123 Main Street'
    })
    assert response.status_code == 200  # Expect validation error, check for flash message.
    assert b'Email already exists.' in response.data

# 13. Test uploading a resume with minimal file content
def test_upload_minimal_content_resume(authenticated_client):
    data = {
        'resume': (BytesIO(b'Minimal Content'), 'minimal_resume.pdf')  # Valid minimal content
    }
    response = authenticated_client.post('/upload_resume', content_type='multipart/form-data', data=data)
    assert response.status_code == 302  # Expect redirect on successful upload

# 14. Test uploading a resume after deleting a previous one
def test_resume_upload_after_deletion(client):
    # First, simulate a resume upload
    upload_response = client.post('/upload_resume', data={
        'resume': (io.BytesIO(b"sample resume content"), 'resume.pdf'),
    })
    assert upload_response.status_code == 302  # Check that the upload was successful

    # Now, simulate deleting the resume
    delete_response = client.post('/delete_resume')  # Adjust the route based on your actual delete implementation
    assert delete_response.status_code == 302  # Check that the delete was successful

    # Attempt to upload again after deletion
    response = client.post('/upload_resume', data={
        'resume': (io.BytesIO(b"new resume content"), 'new_resume.pdf'),
    })
    assert response.status_code == 200  # Check that the upload after deletion is valid
    assert b'Resume uploaded successfully!' in response.data  # Check for success message

# 15. Test updating account with excessive character lengths
def test_update_account_excessive_length(authenticated_client):
    long_string = 'a' * 300  # Assuming 250 is the length limit
    response = authenticated_client.post('/account', data={
        'username': long_string,
        'email': long_string + '@example.com',
        'contact_info': long_string,
        'address': long_string
    })
    assert response.status_code == 200  # Expect validation error

# 16. Test resume upload with files that are too large
def test_resume_upload_large_file(authenticated_client):
    large_content = b'A' * (10 * 1024 * 1024)  # 10 MB content
    data = {
        'resume': (BytesIO(large_content), 'large_resume.pdf')  # Too large
    }
    response = authenticated_client.post('/upload_resume', content_type='multipart/form-data', data=data)
    assert response.status_code == 200  # Expect validation error for file size

# 17. Test unsuccessful login due to wrong password
def test_login_wrong_password():
    response = app.test_client().post('/login', data={'email': 'asavla2@ncsu.edu', 'password': 'wrongpass'})
    assert b'Login Unsuccessful. Please enter correct email and password.' in response.data

# 18. Test unsuccessful login due to unregistered email
def test_login_unregistered_email():
    response = app.test_client().post('/login', data={'email': 'notregistered@ncsu.edu', 'password': 'pass'})
    assert b'Login Unsuccessful. Please enter correct email and password.' in response.data

# 19. Test accessing the profile page when not logged in
def test_profile_access_without_login():
    response = app.test_client().get('/account')
    assert response.status_code == 302  # Expect to be redirected to login

# 20. Test the flash messages for successful file upload
def test_flash_message_successful_upload(authenticated_client):
    data = {
        'resume': (BytesIO(b'Some content'), 'new_resume.pdf')
    }
    response = authenticated_client.post('/upload_resume', content_type='multipart/form-data', data=data)
    with app.test_request_context():
        assert 'Resume uploaded successfully!' in [msg[1] for msg in get_flashed_messages(with_categories=True)]

# 21. Test the flash messages for failed file upload
def test_flash_message_failed_upload(authenticated_client):
    data = {
        'resume': (BytesIO(b''), 'empty_resume.pdf')  # empty file
    }
    response = authenticated_client.post('/upload_resume', content_type='multipart/form-data', data=data)
    with app.test_request_context():
        assert 'Invalid file type. Please upload a PDF or Word document.' in [msg[1] for msg in get_flashed_messages(with_categories=True)]
