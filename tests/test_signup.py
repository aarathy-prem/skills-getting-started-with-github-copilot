def test_signup_success(client):
    """Test successfully signing up for an activity"""
    response = client.post(
        "/activities/Chess Club/signup?email=test@example.com"
    )
    assert response.status_code == 200
    
    data = response.json()
    assert "message" in data
    assert "test@example.com" in data["message"]
    assert "Chess Club" in data["message"]


def test_signup_adds_participant(client):
    """Test that signup adds participant to activity"""
    email = "student@mergington.edu"
    
    response = client.post(
        f"/activities/Programming Class/signup?email={email}"
    )
    assert response.status_code == 200
    
    # Verify participant was added
    response = client.get("/activities")
    activities = response.json()
    assert email in activities["Programming Class"]["participants"]


def test_signup_duplicate_fails(client):
    """Test that signing up twice for same activity fails"""
    email = "student@mergington.edu"
    activity = "Basketball Team"
    
    # First signup
    response = client.post(
        f"/activities/{activity}/signup?email={email}"
    )
    assert response.status_code == 200
    
    # Second signup should fail
    response = client.post(
        f"/activities/{activity}/signup?email={email}"
    )
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_nonexistent_activity(client):
    """Test signing up for non-existent activity"""
    response = client.post(
        "/activities/Nonexistent Club/signup?email=student@example.com"
    )
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_signup_multiple_students(client):
    """Test that multiple students can sign up for same activity"""
    activity = "Programming Class"
    emails = [
        "student1@mergington.edu",
        "student2@mergington.edu",
        "student3@mergington.edu"
    ]
    
    for email in emails:
        response = client.post(
            f"/activities/{activity}/signup?email={email}"
        )
        assert response.status_code == 200
    
    # Verify all students are signed up
    response = client.get("/activities")
    participants = response.json()[activity]["participants"]
    for email in emails:
        assert email in participants
