import pytest
from unittest.mock import MagicMock, patch
import jwt
from datetime import datetime, timedelta


class TestJWTTokenHandler:
    """Test JWT token handler."""
    
    def test_create_access_token(self):
        """Test creating access token."""
        from src.auth.jwt_handler import create_access_token
        
        data = {"sub": "1", "email": "test@example.com"}
        token = create_access_token(data)
        
        assert token is not None
        assert isinstance(token, str)
    
    def test_create_refresh_token(self):
        """Test creating refresh token."""
        from src.auth.jwt_handler import create_refresh_token
        
        data = {"sub": "1", "email": "test@example.com"}
        token = create_refresh_token(data)
        
        assert token is not None
        assert isinstance(token, str)
    
    def test_decode_token(self):
        """Test decoding a token."""
        from src.auth.jwt_handler import create_access_token, decode_token
        
        data = {"sub": "1", "email": "test@example.com"}
        token = create_access_token(data)
        decoded = decode_token(token)
        
        assert decoded is not None
        assert decoded["sub"] == "1"
        assert decoded["email"] == "test@example.com"
    
    def test_verify_token_valid(self):
        """Test verifying valid token."""
        from src.auth.jwt_handler import create_access_token, verify_token
        
        data = {"sub": "1", "email": "test@example.com"}
        token = create_access_token(data)
        verified = verify_token(token, "access")
        
        assert verified is not None
        assert verified["sub"] == "1"
    
    def test_verify_token_invalid_type(self):
        """Test verifying token with wrong type."""
        from src.auth.jwt_handler import create_access_token, verify_token
        
        data = {"sub": "1", "email": "test@example.com"}
        token = create_access_token(data)
        verified = verify_token(token, "refresh")
        
        assert verified is None
    
    def test_verify_token_invalid(self):
        """Test verifying invalid token."""
        from src.auth.jwt_handler import verify_token
        
        verified = verify_token("invalid.token.here", "access")
        
        assert verified is None


class TestPasswordHandler:
    """Test password handler."""
    
    def test_hash_password(self):
        """Test hashing a password."""
        from src.auth.password import hash_password
        
        password = "testpassword123"
        hashed, salt = hash_password(password)
        
        assert hashed is not None
        assert salt is not None
        assert len(salt) > 0
    
    def test_verify_password_correct(self):
        """Test verifying correct password."""
        from src.auth.password import hash_password, verify_password
        
        password = "testpassword123"
        hashed, salt = hash_password(password)
        
        assert verify_password(password, hashed, salt) is True
    
    def test_verify_password_incorrect(self):
        """Test verifying incorrect password."""
        from src.auth.password import hash_password, verify_password
        
        password = "testpassword123"
        wrong_password = "wrongpassword"
        hashed, salt = hash_password(password)
        
        assert verify_password(wrong_password, hashed, salt) is False
    
    def test_generate_random_password(self):
        """Test generating random password."""
        from src.auth.password import generate_random_password
        
        password = generate_random_password(16)
        
        assert len(password) == 16
        assert password != generate_random_password(16)  # Should be unique


class TestStateManager:
    """Test state manager."""
    
    def test_create_task(self):
        """Test creating a task state."""
        from src.orchestrator.state_manager import StateManager, TaskState
        
        manager = StateManager()
        manager.create_task("task_1", TaskState.PENDING)
        
        assert manager.get_state("task_1") == TaskState.PENDING
    
    def test_update_state(self):
        """Test updating task state."""
        from src.orchestrator.state_manager import StateManager, TaskState
        
        manager = StateManager()
        manager.create_task("task_1", TaskState.PENDING)
        result = manager.update_state("task_1", TaskState.RUNNING)
        
        assert result is True
        assert manager.get_state("task_1") == TaskState.RUNNING
    
    def test_get_metadata(self):
        """Test getting task metadata."""
        from src.orchestrator.state_manager import StateManager, TaskState
        
        manager = StateManager()
        manager.create_task("task_1", TaskState.PENDING, {"user": "test"})
        
        metadata = manager.get_metadata("task_1")
        
        assert metadata is not None
        assert "created_at" in metadata
    
    def test_list_tasks_by_state(self):
        """Test listing tasks by state."""
        from src.orchestrator.state_manager import StateManager, TaskState
        
        manager = StateManager()
        manager.create_task("task_1", TaskState.PENDING)
        manager.create_task("task_2", TaskState.PENDING)
        manager.create_task("task_3", TaskState.RUNNING)
        
        pending = manager.list_tasks_by_state(TaskState.PENDING)
        
        assert len(pending) == 2
        assert "task_1" in pending
        assert "task_2" in pending


class TestTaskRouter:
    """Test task router."""
    
    def test_route_task(self):
        """Test routing a task to an agent."""
        from src.orchestrator.task_router import TaskRouter
        
        router = TaskRouter()
        agent = router.route_task("proposal_writing", {})
        
        assert agent == "proposal_agent"
    
    def test_route_task_default(self):
        """Test default routing for unknown task."""
        from src.orchestrator.task_router import TaskRouter
        
        router = TaskRouter()
        agent = router.route_task("unknown_task", {})
        
        assert agent == "pm_agent"  # Default
    
    def test_list_available_agents(self):
        """Test listing available agents."""
        from src.orchestrator.task_router import TaskRouter
        
        router = TaskRouter()
        agents = router.list_available_agents()
        
        assert len(agents) > 0
        assert "pm_agent" in agents
    
    def test_get_capabilities(self):
        """Test getting agent capabilities."""
        from src.orchestrator.task_router import TaskRouter
        
        router = TaskRouter()
        capabilities = router.get_capabilities("pm_agent")
        
        assert "project_planning" in capabilities
        assert "task_management" in capabilities
