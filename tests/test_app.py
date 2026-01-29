import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Basketball Team" in data
    assert "participants" in data["Basketball Team"]

def test_signup_for_activity_success():
    email = "testuser@mergington.edu"
    activity = "Basketball Team"
    # Remove if already present
    client.get("/activities")
    # Try to sign up
    response = client.post(f"/activities/{activity}/signup?email={email}")
    if response.status_code == 400:
        # Already signed up, so remove and try again
        activities[activity]["participants"].remove(email)
        response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert f"Signed up {email} for {activity}" in response.json()["message"]
    # Clean up
    activities[activity]["participants"].remove(email)

def test_signup_for_activity_duplicate():
    email = "alex@mergington.edu"
    activity = "Basketball Team"
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]

def test_signup_for_activity_not_found():
    response = client.post("/activities/Nonexistent/signup?email=someone@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
