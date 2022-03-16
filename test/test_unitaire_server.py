from server import app
import pytest

"""@pytest.mark.parametrize("data", [{
    "competition": "Spring Festival", "club": "Simply Lift", "places": "3" }])"""
def test_booking():
    response = app.test_client().post('/purchasePlaces',
                                      data={"competition": "Spring Festival", "club": "Simply Lift", "places": "3"})
    assert response.status_code == 200
    assert b'Great-booking complete!' in response.data
