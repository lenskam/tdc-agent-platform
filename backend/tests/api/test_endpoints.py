import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient


@pytest.fixture
def mock_db():
    """Mock database session."""
    return MagicMock()


@pytest.fixture
def mock_user():
    """Mock current user."""
    return {"user_id": "1", "email": "test@example.com", "role": "admin"}


class TestHealthEndpoints:
    """Test health check endpoints."""
    
    def test_health_check(self):
        """Test basic health check returns healthy."""
        from src.api.main import app
        
        client = TestClient(app)
        response = client.get("/")
        
        assert response.status_code == 200
        assert "message" in response.json()
    
    def test_health_endpoint_structure(self):
        """Test health endpoint exists."""
        from src.api.main import app
        
        client = TestClient(app)
        
        with patch("src.api.routes.monitoring.get_db") as mock_get_db:
            mock_get_db.return_value = MagicMock()
            response = client.get("/api/v1/health")
            
            assert response.status_code == 200


class TestAuthEndpoints:
    """Test authentication endpoints."""
    
    def test_login_demo_success(self):
        """Test demo login returns tokens."""
        from src.api.main import app
        
        client = TestClient(app)
        response = client.post("/api/v1/auth/login-demo")
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert "user" in data
        assert data["user"]["email"] == "admin@tdc.com"
    
    def test_login_demo_returns_jwt(self):
        """Test demo login returns valid JWT structure."""
        from src.api.main import app
        
        client = TestClient(app)
        response = client.post("/api/v1/auth/login-demo")
        
        assert response.status_code == 200
        data = response.json()
        assert data["token_type"] == "bearer"


class TestTaskEndpoints:
    """Test task endpoints."""
    
    def test_list_tasks_empty(self):
        """Test listing tasks returns empty list."""
        from src.api.main import app
        
        client = TestClient(app)
        response = client.get("/api/v1/tasks/")
        
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_list_tasks_with_params(self):
        """Test listing tasks with filters."""
        from src.api.main import app
        
        client = TestClient(app)
        response = client.get("/api/v1/tasks/?status=done&limit=10")
        
        assert response.status_code == 200


class TestApprovalEndpoints:
    """Test approval endpoints."""
    
    def test_list_approvals_empty(self):
        """Test listing approvals returns empty list."""
        from src.api.main import app
        
        client = TestClient(app)
        response = client.get("/api/v1/approvals/")
        
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_list_pending_approvals(self):
        """Test listing pending approvals."""
        from src.api.main import app
        
        client = TestClient(app)
        response = client.get("/api/v1/approvals/pending")
        
        assert response.status_code == 200
        assert isinstance(response.json(), list)


class TestMetricsEndpoints:
    """Test metrics endpoints."""
    
    def test_metrics_endpoint_exists(self):
        """Test metrics endpoint returns data."""
        from src.api.main import app
        
        client = TestClient(app)
        response = client.get("/api/v1/metrics")
        
        assert response.status_code == 200
        data = response.json()
        assert "tasks" in data or "generated_at" in data
    
    def test_task_metrics_endpoint(self):
        """Test task metrics endpoint."""
        from src.api.main import app
        
        client = TestClient(app)
        response = client.get("/api/v1/metrics/tasks")
        
        assert response.status_code == 200


class TestAuditEndpoints:
    """Test audit endpoints."""
    
    def test_list_audit_logs(self):
        """Test listing audit logs."""
        from src.api.main import app
        
        client = TestClient(app)
        response = client.get("/api/v1/audit/")
        
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_list_auth_logs(self):
        """Test listing auth audit logs."""
        from src.api.main import app
        
        client = TestClient(app)
        response = client.get("/api/v1/audit/auth")
        
        assert response.status_code == 200
