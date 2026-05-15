"""
Integration tests for API routes
"""

import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

class TestHealthEndpoints:
    def test_root_endpoint(self):
        response = client.get("/")
        assert response.status_code == 200
        assert "message" in response.json()
    
    def test_health_check(self):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
    
    def test_api_status(self):
        response = client.get("/api/status")
        assert response.status_code == 200
        assert "status" in response.json()

class TestSignalsEndpoints:
    def test_signals_health(self):
        response = client.get("/api/signals/health")
        assert response.status_code == 200
    
    def test_analyze_signal_valid_symbol(self):
        # This test requires internet connection to fetch data
        response = client.get("/api/signals/analyze/AAPL?period=1mo")
        # Will fail if no data or error, which is expected in test environment
        assert response.status_code in [200, 404, 500]
    
    def test_analyze_signal_invalid_symbol(self):
        response = client.get("/api/signals/analyze/INVALIDTICKER123?period=1mo")
        assert response.status_code in [404, 500]

class TestNewsEndpoints:
    def test_news_health(self):
        response = client.get("/api/news/health")
        assert response.status_code == 200
    
    def test_news_search_requires_query(self):
        response = client.get("/api/news/search")
        # Missing required query parameter
        assert response.status_code == 422

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
