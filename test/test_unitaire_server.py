from server import app
import pytest


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

#testing booking page with mark.parametrize

@pytest.mark.parametrize('data, answer', [
    ({'competition': 'Spring Festival', 'club': 'Iron Temple', 'places': 6},
     b'Solde des points insuffisants'),
    ({'competition': 'Spring Festival', 'club': 'Iron Temple', 'places': 13},
     b'Vous pouvez reserver 12 place maximum'),
    ({'competition': 'Spring Festival', 'club': 'Iron Temple', 'places': 1},
     b'<title>Summary | GUDLFT Registration</title>'),
])
def test_booking(data, answer):
    # shouldn't be able to book more than 12 seats & from whats available
    # Shouldn't be able to book if they don't have enough points (1 point = 1 competition)
    # Shouldn't book a competition if it's date has passed
    response = app.test_client().post('/purchasePlaces', data=data)
    assert response.status_code == 200


@pytest.mark.parametrize("url", ["book/Spring Festival/Iron Temple",
                                 "book/Fall Classic/Iron Temple",
                                 "book/Spring Festival/Simply Lift",])
def test_booking_expired_date(url):

    response = app.test_client().get(url)
    assert response.status_code == 200
    assert b'date de competition expirer' in response.data
