import pytest
from unittest.mock import patch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.models import Base
from src.tools.task_manager import TaskManager, task_manager_tools
from src.database import postgres

# Use in-memory SQLite for testing tools
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency override
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

@pytest.fixture
def test_db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    
    # Patch session in the TOOL module, not just the database module
    # Because task_manager imported it as `from ..database.postgres import SessionLocal`
    # we need to patch specifically where it is used.
    with patch('src.tools.task_manager.SessionLocal', return_value=db):
        yield db
    
    db.close()
    Base.metadata.drop_all(bind=engine)

def test_create_project(test_db):
    result = TaskManager.create_project.invoke({
        "name": "Test Project",
        "description": "A test project",
        "client_name": "Test Client"
    })
    assert "Project created successfully" in result

def test_add_task_to_project(test_db):
    # Create project first
    TaskManager.create_project.invoke({
        "name": "Test Project", 
        "description": "desc", 
        "client_name": "Client"
    })
    
    # Add task (Project ID is likely 1)
    result = TaskManager.add_task_to_project.invoke({
        "project_id": 1,
        "title": "Subtask 1",
        "description": "Do something",
        "assigned_to": "Dev"
    })
    
    assert "added to Project" in result

def test_list_tasks(test_db):
    # Create project
    TaskManager.create_project.invoke({"name": "P1", "description": "d", "client_name": "c"})
    # Add task
    TaskManager.add_task_to_project.invoke({"project_id": 1, "title": "T1", "description": "d"})
    
    result = TaskManager.list_project_tasks.invoke({"project_id": 1})
    assert "T1" in result
    assert "todo" in result
