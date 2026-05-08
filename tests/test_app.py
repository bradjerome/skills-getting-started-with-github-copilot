from urllib.parse import quote


def test_get_activities_returns_activity_data(client):
    # Arrange
    activity_name = "Chess Club"

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert activity_name in data
    assert data[activity_name]["description"] == "Learn strategies and compete in chess tournaments"


def test_signup_adds_participant_to_activity(client):
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    path = f"/activities/{quote(activity_name, safe='')}/signup"

    # Act
    response = client.post(path, params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"
    assert email in client.get("/activities").json()[activity_name]["participants"]


def test_duplicate_signup_returns_400(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    path = f"/activities/{quote(activity_name, safe='')}/signup"

    # Act
    response = client.post(path, params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_unregister_participant_removes_from_activity(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    path = f"/activities/{quote(activity_name, safe='')}/participants"

    # Act
    response = client.delete(path, params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"
    assert email not in client.get("/activities").json()[activity_name]["participants"]


def test_invalid_activity_returns_404(client):
    # Arrange
    activity_name = "Nonexistent Club"
    email = "student@mergington.edu"
    signup_path = f"/activities/{quote(activity_name, safe='')}/signup"
    delete_path = f"/activities/{quote(activity_name, safe='')}/participants"

    # Act
    response_signup = client.post(signup_path, params={"email": email})
    response_delete = client.delete(delete_path, params={"email": email})

    # Assert
    assert response_signup.status_code == 404
    assert response_signup.json()["detail"] == "Activity not found"
    assert response_delete.status_code == 404
    assert response_delete.json()["detail"] == "Activity not found"


def test_unregister_unknown_participant_returns_404(client):
    # Arrange
    activity_name = "Chess Club"
    email = "missing@mergington.edu"
    path = f"/activities/{quote(activity_name, safe='')}/participants"

    # Act
    response = client.delete(path, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
