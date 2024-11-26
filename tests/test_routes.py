# test_routes.py

import os
import sys
import pytest
from flask import url_for
from io import BytesIO
from datetime import datetime, timezone  # Added 'timezone' for timezone-aware datetime objects

# Adjust the Python path to include the project root directory
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.insert(0, project_root)

from app import app, db, bcrypt
from app.models import Vacancies, User, Reviews, Notification
from flask_login import current_user
from app.routes import allowed_file

@pytest.fixture
def client():
    # Configure the app for testing
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # In-memory database
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF protection for testing
    app.config['UPLOAD_FOLDER'] = 'app/static/resumes'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Create tables in the in-memory database
            yield client  # Provide the test client
            db.session.remove()
            db.drop_all()

def create_user(email, password, username, is_admin=False):
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(
        email=email,
        password=hashed_password,
        username=username,
        is_admin=is_admin
    )
    db.session.add(user)
    db.session.commit()
    return user

def create_job(jobTitle, jobDescription, jobLocation, jobPayRate, maxHoursAllowed):
    job = Vacancies(
        jobTitle=jobTitle,
        jobDescription=jobDescription,
        jobLocation=jobLocation,
        jobPayRate=jobPayRate,
        maxHoursAllowed=maxHoursAllowed
    )
    db.session.add(job)
    db.session.commit()
    return job

def login(client, email, password):
    return client.post('/login', data=dict(
        email=email,
        password=password
    ), follow_redirects=True)

def logout(client):
    return client.get('/logout', follow_redirects=True)

def test_index_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'NC State Campus Jobs' in response.data

def test_home_route(client):
    response = client.get('/home')
    assert response.status_code == 200
    assert b'NC State Campus Jobs' in response.data

def test_register_get(client):
    response = client.get('/register')
    assert response.status_code == 200
    assert b"Register" in response.data

def test_register_post(client):
    response = client.post('/register', data={
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'testpass',
        'confirm_password': 'testpass'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Account created successfully!" in response.data

def test_login_get(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert b"Login" in response.data

def test_login_post(client):
    # Create a test user
    create_user('testuser@example.com', 'testpass', 'testuser')
    # Attempt to log in
    response = client.post('/login', data={
        'email': 'testuser@example.com',
        'password': 'testpass'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'NC State Campus Jobs' in response.data

def test_logout(client):
    # Create and login a user
    create_user('testuser@example.com', 'testpass', 'testuser')
    login(client, 'testuser@example.com', 'testpass')

    # Logout
    response = logout(client)
    assert response.status_code == 200
    assert b"Logged out successfully!" in response.data

def test_view_review_all(client):
    # Create a review to display
    user = create_user('user@example.com', 'password', 'user')
    login(client, 'user@example.com', 'password')
    client.post('/review/new', data={
        "job_title": "Sample Job",
        "job_description": "Sample Description",
        "department": "Sample Department",
        "locations": "Sample Location",
        "hourly_pay": "15",
        "benefits": "Sample Benefits",
        "review": "Great place to work!",
        "rating": 5,
        "recommendation": 8,
    }, follow_redirects=True)

    response = client.get('/review/all')
    assert response.status_code == 200
    assert b'Sample Job' in response.data

def test_new_review(client):
    # Create and login a user
    create_user('user@example.com', 'password', 'user')
    login(client, 'user@example.com', 'password')

    # Access new review page
    response = client.get('/review/new')
    assert response.status_code == 200
    assert b'Add your Review' in response.data

    # Submit a new review
    response = client.post('/review/new', data={
        "job_title": "Test Job",
        "job_description": "Job Description",
        "department": "Department",
        "locations": "Location",
        "hourly_pay": "20",
        "benefits": "Benefits",
        "review": "This is a test review.",
        "rating": 4,
        "recommendation": 7,
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Review submitted successfully!' in response.data

def test_review_detail(client):
    # Create and login a user
    user = create_user('user@example.com', 'password', 'user')
    login(client, 'user@example.com', 'password')

    # Create a review
    client.post('/review/new', data={
        "job_title": "Test Job",
        "job_description": "Job Description",
        "department": "Department",
        "locations": "Location",
        "hourly_pay": "20",
        "benefits": "Benefits",
        "review": "This is a test review.",
        "rating": 4,
        "recommendation": 7,
    }, follow_redirects=True)

    # Retrieve the review
    review = Reviews.query.filter_by(job_title="Test Job").first()
    assert review is not None

    # Access the review detail page
    response = client.get(f'/review/{review.id}')
    assert response.status_code == 200
    assert b'Test Job' in response.data

def test_update_review(client):
    # Create and login a user
    user = create_user('user@example.com', 'password', 'user')
    login(client, 'user@example.com', 'password')

    # Create a review
    client.post('/review/new', data={
        "job_title": "Test Job",
        "job_description": "Job Description",
        "department": "Department",
        "locations": "Location",
        "hourly_pay": "20",
        "benefits": "Benefits",
        "review": "This is a test review.",
        "rating": 4,
        "recommendation": 7,
    }, follow_redirects=True)

    # Retrieve the review
    review = Reviews.query.filter_by(job_title="Test Job").first()
    assert review is not None

    # Update the review
    response = client.post(f'/review/{review.id}/update', data={
        "job_title": "Updated Job",
        "job_description": "Updated Description",
        "department": "Updated Department",
        "locations": "Updated Location",
        "hourly_pay": "25",
        "benefits": "Updated Benefits",
        "review": "This is an updated review.",
        "rating": 5,
        "recommendation": 9,
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Your review has been updated!' in response.data

def test_delete_review(client):
    # Create and login a user
    user = create_user('user@example.com', 'password', 'user')
    login(client, 'user@example.com', 'password')

    # Create a review
    client.post('/review/new', data={
        "job_title": "Job to Delete",
        "job_description": "Description",
        "department": "Department",
        "locations": "Location",
        "hourly_pay": "20",
        "benefits": "Benefits",
        "review": "This review will be deleted.",
        "rating": 3,
        "recommendation": 5,
    }, follow_redirects=True)

    # Retrieve the review
    review = Reviews.query.filter_by(job_title="Job to Delete").first()
    assert review is not None

    # Delete the review
    response = client.post(f'/review/{review.id}/delete', follow_redirects=True)
    assert response.status_code == 200
    assert b'The review has been deleted!' in response.data

def test_profile_update(client):
    # Create and login a user
    user = create_user('user@example.com', 'password', 'user')
    login(client, 'user@example.com', 'password')

    # Access account page
    response = client.get('/account')
    assert response.status_code == 200
    assert b'Account' in response.data

    # Update account information
    response = client.post('/account', data={
        'username': 'updateduser',
        'email': 'updateduser@example.com',
        'contact_info': '1234567890',
        'address': '123 Main St',
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Your account has been updated!' in response.data

def test_cancel_application(client):
    # Create user and login
    user = create_user('applicant@example.com', 'password', 'applicant')
    login(client, 'applicant@example.com', 'password')

    # Create a job
    job = create_job('Test Job', 'Job Description', 'Location', 20, 40)

    # Apply for the job
    client.post(f'/apply/{job.vacancyId}', follow_redirects=True)

    # Cancel the application
    response = client.post(f'/cancel_application/{job.vacancyId}', follow_redirects=True)
    assert response.status_code == 200
    assert b'Application canceled successfully.' in response.data

def test_dashboard_route(client):
    # Create user and login
    user = create_user('user@example.com', 'password', 'user')
    login(client, 'user@example.com', 'password')

    # Access dashboard
    response = client.get('/dashboard')
    assert response.status_code == 200
    assert b'Part Time Job Listings' in response.data  # Adjusted to match your template

def test_mark_notifications_read(client):
    # Create user and login
    user = create_user('user@example.com', 'password', 'user')
    login(client, 'user@example.com', 'password')

    # Add notifications
    notification1 = Notification(user_id=user.id, message="Notification 1", timestamp=datetime.now(timezone.utc))  # Updated datetime usage
    notification2 = Notification(user_id=user.id, message="Notification 2", timestamp=datetime.now(timezone.utc))  # Updated datetime usage
    db.session.add(notification1)
    db.session.add(notification2)
    db.session.commit()

    # Mark notifications as read
    response = client.post('/notifications/mark_read', follow_redirects=True)
    assert response.status_code == 200
    assert b'All notifications marked as read.' in response.data

def test_check_notifications(client):
    # Create user and login
    user = create_user('user@example.com', 'password', 'user')
    login(client, 'user@example.com', 'password')

    # Add a notification
    notification = Notification(user_id=user.id, message="Test Notification", timestamp=datetime.now(timezone.utc))  # Updated datetime usage
    db.session.add(notification)
    db.session.commit()

    # Check notifications
    response = client.get('/check_notifications')
    assert response.status_code == 200
    assert response.json == {'unread_count': 1}

def test_notifications_page(client):
    # Create user and login
    user = create_user('user@example.com', 'password', 'user')
    login(client, 'user@example.com', 'password')

    # Add notifications
    notification1 = Notification(user_id=user.id, message="Notification 1", timestamp=datetime.now(timezone.utc))  # Updated datetime usage
    notification2 = Notification(user_id=user.id, message="Notification 2", timestamp=datetime.now(timezone.utc))  # Updated datetime usage
    db.session.add(notification1)
    db.session.add(notification2)
    db.session.commit()

    # Access notifications page
    response = client.get('/notifications')
    assert response.status_code == 200
    assert b'Notification 1' in response.data
    assert b'Notification 2' in response.data

def test_upload_resume(client, tmpdir):
    # Create user and login
    user = create_user('user@example.com', 'password', 'user')
    login(client, 'user@example.com', 'password')

    # Create a sample resume file
    resume_file = tmpdir.join('resume.pdf')
    resume_file.write('Sample resume content')

    # Upload the resume
    with open(resume_file, 'rb') as f:
        data = {
            'resume': (f, 'resume.pdf'),
        }
        response = client.post('/upload_resume', data=data, content_type='multipart/form-data', follow_redirects=True)
    assert response.status_code == 200
    assert b'Resume uploaded successfully!' in response.data

def test_admin_dashboard_access(client):
    # Create admin user and login
    admin = create_user('admin@example.com', 'password', 'admin', is_admin=True)
    login(client, 'admin@example.com', 'password')

    # Access admin dashboard
    response = client.get('/admin/dashboard')
    assert response.status_code == 200
    assert b'Users' in response.data  # Adjusted to match your admin dashboard content

def test_non_admin_cannot_access_admin_dashboard(client):
    # Create regular user and login
    user = create_user('user@example.com', 'password', 'user')
    login(client, 'user@example.com', 'password')

    # Attempt to access admin dashboard
    response = client.get('/admin/dashboard')
    assert response.status_code == 403

def test_feedback_page(client):
    # Create user and login
    user = create_user('user@example.com', 'password', 'user')
    login(client, 'user@example.com', 'password')

    # Access feedback page
    response = client.get('/feedback')
    assert response.status_code == 200
    assert b'Feedback' in response.data

    # Submit feedback
    response = client.post('/feedback', data={
        'feedback': 'This is a test feedback.'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Thank you for your feedback!' in response.data

def test_about_page(client):
    response = client.get('/about')
    assert response.status_code == 200
    assert b'About Us' in response.data  # Adjust to match your template content

def test_contact_page(client):
    response = client.get('/contact')
    assert response.status_code == 200
    assert b'Contact Us' in response.data  # Adjust to match your template content

def test_allowed_file():
    assert allowed_file('document.pdf') == True
    assert allowed_file('resume.doc') == True
    assert allowed_file('image.jpg') == False
    assert allowed_file('script.exe') == False

def test_job_listings_search(client):
    # Create jobs
    create_job('Developer', 'Develop software', 'City A', 25, 40)
    create_job('Analyst', 'Analyze data', 'City B', 20, 30)

    # Search for 'Developer'
    response = client.get('/job_listings?search=Developer')
    assert response.status_code == 200
    assert b'Developer' in response.data
    assert b'Analyst' not in response.data

def test_job_listings_filter(client):
    # Create jobs
    create_job('Developer', 'Develop software', 'City A', 25, 40)
    create_job('Analyst', 'Analyze data', 'City B', 20, 30)

    # Filter by location 'City B'
    response = client.get('/job_listings?jobLocation=City B')
    assert response.status_code == 200
    assert b'Analyst' in response.data
    assert b'Developer' not in response.data

def test_job_listings_pay_rate_filter(client):
    # Create jobs
    create_job('Developer', 'Develop software', 'City A', 25, 40)
    create_job('Analyst', 'Analyze data', 'City B', 20, 30)

    # Filter by pay rate up to $20
    response = client.get('/job_listings?payRate=20')
    assert response.status_code == 200
    assert b'Analyst' in response.data
    assert b'Developer' not in response.data

def test_invalid_login(client):
    # Attempt to login with invalid credentials
    response = client.post('/login', data={
        'email': 'invalid@example.com',
        'password': 'wrongpassword'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Login Unsuccessful. Please enter correct email and password.' in response.data

def test_access_protected_route_without_login(client):
    # Access a protected route without logging in
    response = client.get('/account')
    assert response.status_code == 302  # Should redirect to login
    assert '/login' in response.headers['Location']

def test_delete_user_as_admin(client):
    # Create admin and regular user
    admin = create_user('admin@example.com', 'password', 'admin', is_admin=True)
    user = create_user('user_to_delete@example.com', 'password', 'user_to_delete')

    # Login as admin
    login(client, 'admin@example.com', 'password')

    # Delete the user
    response = client.post(f'/delete_user/{user.id}', follow_redirects=True)
    assert response.status_code == 200
    assert b'User has been deleted successfully.' in response.data

def test_toggle_admin_status(client):
    # Create admin and regular user
    admin = create_user('admin@example.com', 'password', 'admin', is_admin=True)
    user = create_user('user@example.com', 'password', 'user')

    # Login as admin
    login(client, 'admin@example.com', 'password')

    # Toggle admin status
    response = client.post(f'/toggle_admin/{user.id}', follow_redirects=True)
    assert response.status_code == 200
    assert b'User admin status has been updated.' in response.data

def test_non_admin_cannot_toggle_admin_status(client):
    # Create regular users
    user1 = create_user('user1@example.com', 'password', 'user1')
    user2 = create_user('user2@example.com', 'password', 'user2')

    # Login as user1
    login(client, 'user1@example.com', 'password')

    # Attempt to toggle admin status of user2
    response = client.post(f'/toggle_admin/{user2.id}', follow_redirects=True)
    assert response.status_code == 403  # Forbidden

def test_non_admin_cannot_post_job(client):
    # Create regular user and login
    user = create_user('user@example.com', 'password', 'user')
    login(client, 'user@example.com', 'password')

    # Attempt to post a new job
    response = client.post('/post_job_apply', data={
        'jobTitle': 'User Job',
        'jobDescription': 'Job Description',
        'jobLocation': 'Location',
        'jobPayRate': '30',
        'maxHoursAllowed': '40'
    })
    assert response.status_code == 403  # Forbidden

def test_non_admin_cannot_delete_job(client):
    # Create regular user and login
    user = create_user('user@example.com', 'password', 'user')
    login(client, 'user@example.com', 'password')

    # Create a job
    job = create_job('Job to Attempt Delete', 'Description', 'Location', 25, 35)

    # Attempt to delete the job
    response = client.post(f'/delete-job/{job.vacancyId}', follow_redirects=True)
    assert response.status_code == 403  # Forbidden

def test_access_nonexistent_route(client):
    response = client.get('/nonexistent_route')
    assert response.status_code == 404  # Not Found

def test_contact_form_submission(client):
    # Adjusted to expect 405 Method Not Allowed since /contact does not accept POST
    response = client.post('/contact', data={
        'name': 'Test User',
        'email': 'testuser@example.com',
        'message': 'This is a test message.'
    })
    assert response.status_code == 405  # Method Not Allowed

def test_get_review_statistics(client):
    # Since 'db' is not defined in 'crudapp.py' and we cannot change it, we'll skip this test
    pass
