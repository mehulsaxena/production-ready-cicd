import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestAPI:
    def test_root_endpoint(self):
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "features" in data
        assert "tech_stack" in data
        assert data["version"] == "1.0.0"

    def test_health_endpoint(self):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert "uptime" in data
        assert "python_version" in data
        assert isinstance(data["uptime"], float)

    def test_status_endpoint(self):
        response = client.get("/api/status")
        assert response.status_code == 200
        data = response.json()
        assert data["service"] == "python-demo-app"
        assert data["status"] == "running"
        assert data["version"] == "1.0.0"
        assert "timestamp" in data
        assert "python_version" in data

    def test_metrics_endpoint(self):
        response = client.get("/api/metrics")
        assert response.status_code == 200
        data = response.json()
        assert "uptime_seconds" in data
        assert "uptime_human" in data
        assert "python_info" in data
        assert isinstance(data["uptime_seconds"], float)

    def test_docs_endpoint(self):
        response = client.get("/docs")
        assert response.status_code == 200

    def test_not_found_endpoint(self):
        response = client.get("/nonexistent")
        assert response.status_code == 404
        data = response.json()
        assert "error" in data["detail"]
        assert "available_endpoints" in data["detail"]


class TestHealthChecks:
    def test_health_response_structure(self):
        response = client.get("/health")
        data = response.json()
        required_fields = [
            "status",
            "timestamp",
            "uptime",
            "environment",
            "python_version",
        ]
        for field in required_fields:
            assert field in data

    def test_status_response_structure(self):
        response = client.get("/api/status")
        data = response.json()
        required_fields = [
            "service",
            "status",
            "timestamp",
            "version",
            "python_version",
            "platform",
        ]
        for field in required_fields:
            assert field in data


@pytest.mark.asyncio
async def test_concurrent_requests():
    import asyncio
    import httpx

    async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
        tasks = [ac.get("/health") for _ in range(10)]
        responses = await asyncio.gather(*tasks)

    for response in responses:
        assert response.status_code == 200
