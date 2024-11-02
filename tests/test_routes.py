import os
import sys
from flask import render_template, request, redirect, flash, url_for, abort
import pytest
sys.path.append(os.path.join(os.getcwd(), "app"))
from app import app,db
from app.models import Vacancies, User

@pytest.fixture
def client():
    # Use an in-memory database for testing
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # In-memory database
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Create database tables in the in-memory database
            yield client  # Provide the test client for tests
            db.drop_all()

def create_test_user():
    user = User(
        email="existing@example.com", 
        password="password",
        username="testuser",
        is_admin=False
    )
    db.session.add(user)
    db.session.commit()
    return user

def create_test_job():
    job = Vacancies(
        jobTitle="Test Job", 
        jobDescription="Job description", 
        jobLocation="Location", 
        jobPayRate="50000", 
        maxHoursAllowed=40 
    )
    db.session.add(job)
    db.session.commit()
    return job

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

def test_dashboard_route(client):
    response = client.get('/dashboard')
    assert response.status_code == 200

def test_account_route(client):
    response = client.get('/account')
    assert response.status_code == 302

def test_admin_access_denied(client):
    # Manually log in as a regular user
    client.post("/login", data={"email": "regularuser@example.com", "password": "userpass"})
    response = client.get("/admin/dashboard")
    assert response.status_code == 302
    assert '/login' in response.headers['Location'] 

def test_register_existing_email(client):
    # Register the first time
    response1 = client.post("/register", data={
        "username": "newuser",
        "email": "test1@example.com",
        "password": "password",
        "confirm_password": "password",
        "is_admin": False
    })
    assert response1.status_code == 200
    
    # Try to register again with the same email
    response2 = client.post("/register", data={
        "username": "newuser2",
        "email": "existing@example.com",  # Same email as before
        "password": "password",
        "confirm_password": "password",
        "is_admin": False
    })
    assert response1.status_code == 200 


def test_view_nonexistent_review(client):
    response = client.get("/review/999")
    assert response.status_code == 404

def test_edit_review_forbidden(client):
    # Manually log in a regular user
    client.post("/login", data={"email": "regularuser@example.com", "password": "userpass"})
    # Attempt to edit a review as a regular user (should be forbidden)
    response = client.post("/review/1/update", data={"review": "Updated review content"})
    assert response.status_code == 302 #redirected to the login.html page again


def test_delete_review_admin(client):
    # Manually log in as an admin
    client.post("/login", data={"email": "admin@example.com", "password": "adminpass"})
    response = client.post("/review/1/delete")
    assert response.status_code == 302

def test_review_pagination(client):
    response = client.get("/review/all?page=2")
    assert response.status_code == 200
def test_dashboard_route(client):
    response = client.get('/dashboard')
    assert response.status_code == 200

def test_account_route(client):
    response = client.get('/account')
    assert response.status_code == 302

def test_admin_access_denied(client):
    # Manually log in as a regular user
    client.post("/login", data={"email": "regularuser@example.com", "password": "userpass"})
    response = client.get("/admin/dashboard")
    assert response.status_code == 302
    assert '/login' in response.headers['Location'] 

def test_register_existing_email(client):
    # Register the first time
    response1 = client.post("/register", data={
        "username": "newuser",
        "email": "test1@example.com",
        "password": "password",
        "confirm_password": "password",
        "is_admin": False
    })
    assert response1.status_code == 200
    
    # Try to register again with the same email
    response2 = client.post("/register", data={
        "username": "newuser2",
        "email": "existing@example.com",  # Same email as before
        "password": "password",
        "confirm_password": "password",
        "is_admin": False
    })
    assert response1.status_code == 200 


def test_view_nonexistent_review(client):
    response = client.get("/review/999")
    assert response.status_code == 404

def test_edit_review_forbidden(client):
    # Manually log in a regular user
    client.post("/login", data={"email": "regularuser@example.com", "password": "userpass"})
    # Attempt to edit a review as a regular user (should be forbidden)
    response = client.post("/review/1/update", data={"review": "Updated review content"})
    assert response.status_code == 302 #redirected to the login.html page again


def test_delete_review_admin(client):
    # Manually log in as an admin
    client.post("/login", data={"email": "admin@example.com", "password": "adminpass"})
    response = client.post("/review/1/delete")
    assert response.status_code == 302

def test_review_pagination(client):
    response = client.get("/review/all?page=2")
    assert response.status_code == 200

def test_delete_job_admin(client):
    # Manually log in as an admin
    client.post("/login", data={"email": "admin@example.com", "password": "adminpass"})
    response = client.post("/delete-job/1")
    assert response.status_code == 302

def test_empty_job_listing(client):
    response = client.get("/dashboard")
def test_delete_job_admin(client):
    # Manually log in as an admin
    client.post("/login", data={"email": "admin@example.com", "password": "adminpass"})
    response = client.post("/delete-job/1")
    assert response.status_code == 302

def test_empty_job_listing(client):
    response = client.get("/dashboard")
    assert response.status_code == 200

def test_homepage_content(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Reviews" in response.data

def test_toggle_admin_status(client):
    # Manually log in as an admin
    client.post("/login", data={"email": "admin@example.com", "password": "adminpass"})
    # Attempt to toggle admin status
    response = client.post("/toggle_admin/2")
    # Expecting a redirect (302)
    assert response.status_code == 302
    # Follow the redirect to the next page
    redirected_response = client.get(response.location)  # Get the redirected page

def test_admin_delete_user(client):
    # Manually log in as an admin
    client.post("/login", data={"email": "admin@example.com", "password": "adminpass"})
    # Attempt to delete a user
    response = client.post("/delete_user/2")
    # Expecting a redirect (302)
    assert response.status_code == 302

def test_admin_dashboard_content(client):
    # Manually log in as an admin
    response_login = client.post("/login", data={"email": "admin@example.com", "password": "adminpass"})
    # Check if login was successful
    assert response_login.status_code == 200  # Expecting a redirect after successful login
    # Now access the admin dashboard
    response = client.get("/admin/dashboard")
   

def test_admin_can_post_job(client):
    # Manually log in as an admin
    response_login = client.post("/login", data={"email": "admin@example.com", "password": "adminpass"})
    assert response_login.status_code == 200
    
    # Now attempt to post a job
    response = client.post("/post-job", data={
        "jobTitle": "Data Analyst",
        "jobDescription": "Analyze data",
        "jobLocation": "Talley",
        "jobPayRate": "40.0",
        "maxHoursAllowed": "30"
    })
    
    # Assert the response status code for the job posting
    assert response.status_code == 302 

def test_job_deletion_removes_from_listings(client):
    # Manually log in as an admin
    client.post("/login", data={"email": "admin@example.com", "password": "adminpass"})
    client.post("/delete-job/1")  # Assuming job with ID 1 exists
    response = client.get("/job_listings")
    assert b"Software Developer" not in response.data

def test_user_account_update(client):
    # Create a test user
    create_test_user()
    
    # Log in the user
    client.post('/login', data={'email': 'existing@example.com', 'password': 'password'})
    
    # Update account details
    response = client.post('/account', data={
        'username': 'updateduser',
        'email': 'updated@example.com',
        'password': 'newpassword'
    })
    
    assert response.status_code == 302 

def test_job_posting_visibility(client):
    # Create a test user and log them in
    create_test_user()
    client.post('/login', data={'email': 'existing@example.com', 'password': 'password'})
    
    # Create a test job
    job = create_test_job()

    # Access the dashboard
    response = client.get('/dashboard')
    assert job.jobTitle.encode() in response.data

def test_successful_logout(client):
    create_test_user()
    client.post('/login', data={'email': 'existing@example.com', 'password': 'password'})
    
    # Log out the user
    response = client.get('/logout')
    assert response.status_code == 302  # Expecting a redirect after logging out

def test_view_nonexistent_job(client):
    response = client.get('/job/999')  # Assuming job ID 999 does not exist
    assert response.status_code == 404