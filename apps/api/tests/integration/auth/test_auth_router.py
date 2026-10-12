"""
Integration tests for Auth API endpoints (/api/v1/auth/*).
"""

from factories.user_factory import UserFactory


def test_auth_login_and_cookie_dispatch(client, db_session):
    UserFactory.create(
        db_session, email="taxpro@smartgst.in", password="ValidPassword123!", role="ADMIN"
    )

    response = client.post(
        "/api/v1/auth/login", json={"email": "taxpro@smartgst.in", "password": "ValidPassword123!"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["role"] == "ADMIN"
    assert "access_token" in response.cookies


def test_auth_login_invalid_credentials(client):
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "nonexistent@smartgst.in", "password": "WrongPassword!"},
    )
    assert response.status_code == 401
    err = response.json()
    assert err["code"] == "UNAUTHORIZED"
    assert "request_id" in err


def test_auth_me_endpoint(client, auth_headers):
    response = client.get("/api/v1/auth/me", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["role"] == "ADMIN"
