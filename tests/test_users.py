import pytest
import requests
import responses

BASE_URL = "http://127.0.0.1:8000/users"

# Test case for invalid credentials
@pytest.mark.parametrize(
    "username, password, expected_status_code, expected_response",
    [
        ("admin", "admin", 401, ""),  # Invalid credentials, expects 401
    ],
)
@responses.activate
def test_users_endpoint_invalid_credentials_mocked(username, password, expected_status_code, expected_response):
    # Define the mocked endpoint and response
    responses.add(
        responses.GET,
        BASE_URL,
        body="",  # Empty body as response
        status=401,  # Unauthorized status
        match=[responses.matchers.query_param_matcher({"username": username, "password": password})],  # Match query parameters
    )

    # Make the GET request with query parameters
    response = requests.get(BASE_URL, params={"username": username, "password": password})

    # Assert status code
    assert response.status_code == expected_status_code, f"Expected {expected_status_code}, got {response.status_code}"

    # Assert response body
    assert response.text == expected_response, f"Expected response body '{expected_response}', got '{response.text}'"


# Test case for valid credentials
@pytest.mark.parametrize(
    "username, password, expected_status_code, expected_response",
    [
        ("admin", "qwerty", 200, ""),  # Valid credentials, expects 200
    ],
)
@responses.activate
def test_users_endpoint_valid_credentials_mocked(username, password, expected_status_code, expected_response):
    # Define the mocked endpoint and response
    responses.add(
        responses.GET,
        BASE_URL,
        body="",  # Empty body as response
        status=200,  # OK status
        match=[responses.matchers.query_param_matcher({"username": username, "password": password})],  # Match query parameters
    )

    # Make the GET request with query parameters
    response = requests.get(BASE_URL, params={"username": username, "password": password})

    # Assert status code
    assert response.status_code == expected_status_code, f"Expected {expected_status_code}, got {response.status_code}"

    # Assert response body
    assert response.text == expected_response, f"Expected response body '{expected_response}', got '{response.text}'"
    