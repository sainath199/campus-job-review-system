import os
import sys

sys.path.append(os.getcwd()[:-5]+"app")
from app import app 

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