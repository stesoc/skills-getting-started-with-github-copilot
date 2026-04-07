import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    # Arrange: No specific setup needed as activities are predefined
    
    # Act: Make GET request to /activities
    response = client.get("/activities")
    
    # Assert: Check status code and response structure
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data
    # Check structure of one activity
    chess_club = data["Chess Club"]
    assert "description" in chess_club
    assert "schedule" in chess_club
    assert "max_participants" in chess_club
    assert "participants" in chess_club
    assert isinstance(chess_club["participants"], list)

def test_signup_success():
    # Arrange: Choose an activity and email not already signed up
    activity = "Basketball Team"
    email = "newstudent@mergington.edu"
    
    # Act: Make POST request to signup
    response = client.post(f"/activities/{activity}/signup?email={email}")
    
    # Assert: Check success response
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert f"Signed up {email} for {activity}" in data["message"]
    
    # Verify the participant was added
    get_response = client.get("/activities")
    activities = get_response.json()
    assert email in activities[activity]["participants"]

def test_signup_duplicate():
    # Arrange: Sign up first, then try again
    activity = "Soccer Club"
    email = "duplicate@mergington.edu"
    client.post(f"/activities/{activity}/signup?email={email}")  # First signup
    
    # Act: Try to signup again
    response = client.post(f"/activities/{activity}/signup?email={email}")
    
    # Assert: Should fail with 400
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "already signed up" in data["detail"]

def test_signup_invalid_activity():
    # Arrange: Use non-existent activity
    invalid_activity = "NonExistent Club"
    email = "test@mergington.edu"
    
    # Act: Make POST request
    response = client.post(f"/activities/{invalid_activity}/signup?email={email}")
    
    # Assert: Should fail with 404
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Activity not found" in data["detail"]

def test_unregister_success():
    # Arrange: Sign up first, then unregister
    activity = "Debate Club"
    email = "unregister@mergington.edu"
    client.post(f"/activities/{activity}/signup?email={email}")  # Signup
    
    # Act: Unregister
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    
    # Assert: Success
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert f"Unregistered {email} from {activity}" in data["message"]
    
    # Verify removed
    get_response = client.get("/activities")
    activities = get_response.json()
    assert email not in activities[activity]["participants"]

def test_unregister_not_registered():
    # Arrange: Try to unregister without being signed up
    activity = "History Society"
    email = "notregistered@mergington.edu"
    
    # Act: Unregister
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    
    # Assert: Fail with 400
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "not registered" in data["detail"]

def test_unregister_invalid_activity():
    # Arrange: Use non-existent activity
    invalid_activity = "Invalid Club"
    email = "test@mergington.edu"
    
    # Act: Make DELETE request
    response = client.delete(f"/activities/{invalid_activity}/unregister?email={email}")
    
    # Assert: Fail with 404
    data = response.json()
    assert "detail" in data
    assert "Activity not found" in data["detail"]
