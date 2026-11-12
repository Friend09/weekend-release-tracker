"""Test release identity and the public conversion API contract."""

import pytest

from app import create_app


@pytest.mark.parametrize("environment", ["local", "development", "production"])
def test_health_identity(monkeypatch, environment):
    """Expose the configured environment and revision for deployment checks."""
    monkeypatch.setenv("APP_ENV", environment)
    monkeypatch.setenv("RENDER_GIT_COMMIT", "abc123")
    response = create_app().test_client().get("/health")
    assert response.status_code == 200
    assert response.get_json() == {
        "status": "ok",
        "environment": environment,
        "commit": "abc123",
    }


def test_release_message():
    """Keep the visible release message intentional."""
    response = create_app().test_client().get("/")
    assert response.status_code == 200
    assert response.get_json()["message"] == "Hello from release 1"


@pytest.mark.parametrize("minutes, expected", [(0, 0.0), (90, 1.5), (1440, 24.0)])
def test_minutes_to_hours(minutes, expected):
    """Convert representative and boundary values correctly."""
    response = create_app().test_client().get(f"/api/hours?minutes={minutes}")
    assert response.status_code == 200
    assert response.get_json() == {"minutes": minutes, "hours": expected}


@pytest.mark.parametrize("value", ["", "nope", "1.5", "-1", "1441"])
def test_invalid_minutes(value):
    """Reject missing, noninteger, and out-of-range input."""
    response = create_app().test_client().get(f"/api/hours?minutes={value}")
    assert response.status_code == 400
    assert "error" in response.get_json()
