from server import app
import pytest

@pytest.mark.parametrize("url", ["book/Spring Festival/Iron Temple",
                                 "book/Fall Classic/Iron Temple",
                                 "book/Spring Festival/Simply Lift",])
def test_booking(url):
    # shouldn't be able to book more than 12 seats & from whats available
    # Shouldn't be able to book if they don't have enough points (1 point = 1 competition)
    # Shouldn't book a competition if it's date has passed

    response = app.test_client().get(url)
    assert response.status_code == 200
    assert b'date de competition expirer' in response.data


