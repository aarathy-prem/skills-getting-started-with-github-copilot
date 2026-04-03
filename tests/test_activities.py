def test_get_activities(client):
    """Test retrieving all activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Basketball Team" in data


def test_get_activities_contains_required_fields(client):
    """Test that activities have required fields"""
    response = client.get("/activities")
    activities = response.json()
    
    for activity_name, activity in activities.items():
        assert "description" in activity
        assert "schedule" in activity
        assert "max_participants" in activity
        assert "participants" in activity
        assert isinstance(activity["participants"], list)
