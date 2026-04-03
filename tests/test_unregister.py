def test_unregister_success(client):
    """Test successfully unregistering from an activity"""
    email = "student@mergington.edu"
    activity = "Chess Club"
    
    # Sign up first
    client.post(f"/activities/{activity}/signup?email={email}")
    
    # Unregister
    response = client.delete(
        f"/activities/{activity}/signup?email={email}"
    )
    assert response.status_code == 200
    
    data = response.json()
    assert "message" in data
    assert email in data["message"]


def test_unregister_removes_participant(client):
    """Test that unregister removes participant from activity"""
    email = "student@mergington.edu"
    activity = "Programming Class"
    
    # Sign up
    client.post(f"/activities/{activity}/signup?email={email}")
    
    # Verify signed up
    response = client.get("/activities")
    assert email in response.json()[activity]["participants"]
    
    # Unregister
    client.delete(f"/activities/{activity}/signup?email={email}")
    
    # Verify removed
    response = client.get("/activities")
    assert email not in response.json()[activity]["participants"]


def test_unregister_not_signed_up(client):
    """Test unregistering when not signed up fails"""
    response = client.delete(
        "/activities/Chess Club/signup?email=notregistered@example.com"
    )
    assert response.status_code == 400
    assert "not signed up" in response.json()["detail"]


def test_unregister_nonexistent_activity(client):
    """Test unregistering from non-existent activity"""
    response = client.delete(
        "/activities/Nonexistent Club/signup?email=student@example.com"
    )
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_signup_unregister_workflow(client):
    """Test complete signup and unregister workflow"""
    email = "workflow@mergington.edu"
    activity = "Basketball Team"
    
    # Sign up
    response = client.post(
        f"/activities/{activity}/signup?email={email}"
    )
    assert response.status_code == 200
    
    # Verify signed up
    response = client.get("/activities")
    assert email in response.json()[activity]["participants"]
    
    # Unregister
    response = client.delete(
        f"/activities/{activity}/signup?email={email}"
    )
    assert response.status_code == 200
    
    # Verify can sign up again
    response = client.post(
        f"/activities/{activity}/signup?email={email}"
    )
    assert response.status_code == 200
