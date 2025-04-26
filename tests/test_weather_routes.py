import pytest
from unittest.mock import patch

# Patch 'requests.get' where it is used
@patch('app.routes.ho_weather.routes.requests.get')
def test_weather_page_loads(mock_get, client):
    # Mock a fake API response
    mock_response = {
        "coord": {"lon": -82.5918, "lat": 28.1939},
        "weather": [{"id": 800, "main": "Clear", "description": "clear sky", "icon": "01d"}],
        "main": {"temp": 75.0, "feels_like": 74.5, "humidity": 40, "pressure": 1015},
        "wind": {"speed": 5.0, "deg": 90},
        "clouds": {"all": 1},
        "dt": 1726660758,
        "sys": {"country": "US"},
        "timezone": -14400,
        "id": 1,
        "name": "Odessa",
        "cod": 200
    }

    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_response

    # Now call the weather page
    response = client.get('/weather/', follow_redirects=True)

    assert response.status_code == 200
    assert b'Odessa' in response.data
    assert b'Clear' in response.data
    assert b'75.0' in response.data

# Simulated failure: API returns an error
@patch('app.routes.ho_weather.routes.requests.get')
def test_weather_page_handles_api_failure(mock_get, client):
    mock_get.side_effect = Exception("Mocked API failure")

    response = client.get('/weather/', follow_redirects=True)

    assert response.status_code == 200
    assert b'Error fetching weather data' in response.data