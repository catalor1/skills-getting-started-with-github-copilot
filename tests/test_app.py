import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# Arrange-Act-Assert: Test GET /activities
def test_get_activities():
    # Arrange: nothing needed, just client
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Soccer Team" in data

# Arrange-Act-Assert: Test POST /activities/{activity_name}/signup
def test_signup_for_activity():
    # Arrange
    activity = "Soccer Team"
    email = "testuser@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert f"Signed up {email} for {activity}" in response.json()["message"]
    # Clean up: remove test user
    client.delete(f"/activities/{activity}/unregister?email={email}")

# Arrange-Act-Assert: Test DELETE /activities/{activity_name}/unregister
def test_unregister_from_activity():
    # Arrange
    activity = "Soccer Team"
    email = "testuser2@mergington.edu"
    # Add user first
    client.post(f"/activities/{activity}/signup?email={email}")
    # Act
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert response.status_code == 200
    assert f"Unregistered {email} from {activity}" in response.json()["message"]

# Arrange-Act-Assert: Test error on duplicate signup
def test_signup_duplicate():
    activity = "Soccer Team"
    email = "testuser3@mergington.edu"
    client.post(f"/activities/{activity}/signup?email={email}")
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    assert "Student already signed up" in response.json()["detail"]
    # Clean up
    client.delete(f"/activities/{activity}/unregister?email={email}")

# Arrange-Act-Assert: Test error on removing non-existent participant
def test_unregister_nonexistent():
    activity = "Soccer Team"
    email = "notfound@mergington.edu"
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 404
    assert "Participant not found" in response.json()["detail"]
