from server import app
import pytest

#testing booking page with mark.parametrize

@pytest.mark.parametrize('data, answer', [
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
    assert answer in response.data