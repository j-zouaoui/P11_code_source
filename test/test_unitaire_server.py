from server import app


#unit test for dosplaying index route
def test_index_route():
    response = app.test_client().get('/')
    assert response.status_code == 200
    #assert response.data.decode('utf-8') == 'Testing, Flask!' failed
    assert b'Welcome to the GUDLFT Registration Portal!' in response.data
    assert b' Please enter your secretary email to continue:' in response.data
    assert b'Enter' in response.data

#test login with known email adress
def test_showSummary_known_email():
    response = app.test_client().post('/showSummary', data={
        "email": "admin@irontemple.com"})
    assert response.status_code == 200
    assert b'Welcome'

#test login with unknown email adress
def test_showSummary_unknown_email():
    response = app.test_client().post('/showSummary', data={
        "email": "testing@irontemple.com"})
    assert response.status_code == 200
    assert b'unknown mail' in response.data

#test login with uncomlet email adress
def test_showSummary_uncomplete_email():
    response = app.test_client().post('/showSummary', data={
        "email": "testing"})
    assert response.status_code == 200



def test_logout():
    """Make sure login and logout works."""
    response = app.test_client().get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'Please enter your secretary email to continue' in response.data
