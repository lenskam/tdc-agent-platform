from typing import Dict, Optional, List
from datetime import datetime
from enum import Enum


class TaskState(str, Enum):
    PENDING = "pending"
    QUEUED = "queued"
    RUNNING = "running"
    WAITING_APPROVAL = "waiting_approval"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class StateManager:
    def __init__(self):
        self._states: Dict[str, TaskState] = {}
        self._metadata: Dict[str, Dict] = {}

    def create_task(self, task_id: str, initial_state: TaskState = TaskState.PENDING, metadata: Optional[Dict] = None):
        """
        Create a new task state entry.
        
        Args:
            task_id: Unique identifier for the task
            initial_state: Initial state of the task
            metadata: Optional metadata for the task
        """
        self._states[task_id] = initial_state
        self._metadata[task_id] = {
            **(metadata or {}),
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "history": [{"state": initial_state, "timestamp": datetime.now().isoformat()}]
        }

    def get_state(self, task_id: str) -> Optional[TaskState]:
        """
        Get the current state of a task.
        
        Args:
            task_id: The task identifier
            
        Returns:
            The current state of the task, or None if not found
        """
        return self._states.get(task_id)

    def update_state(self, task_id: str, new_state: TaskState) -> bool:
        """
        Update the state of a task.
        
        Args:
            task_id: The task identifier
            new_state: The new state to set
            
        Returns:
            True if successful, False if task not found
        """
        if task_id not in self._states:
            return False
            
        old_state = self._states[task_id]
        self._states[task_id] = new_state
        
        if task_id in self._metadata:
            self._metadata[task_id]["updated_at"] = datetime.now().isoformat()
            self._metadata[task_id]["history"].append({
                "from_state": old_state,
                "to_state": new_state,
                "timestamp": datetime.now().isoformat()
            })
        
        return True

    def get_metadata(self, task_id: str) -> Optional[Dict]:
        """
        Get metadata for a task.
        
        Args:
            task_id: The task identifier
            
        Returns:
            The metadata dictionary, or None if not found
        """
        return self._metadata.get(task_id)

    def update_metadata(self, task_id: str, metadata: Dict) -> bool:
        """
        Update metadata for a task.
        
        Args:
            task_id: The task identifier
            metadata: The metadata to merge
            
        Returns:
            True if successful, False if task not found
        """
        if task_id not in self._metadata:
            return False
            
        self._metadata[task_id].update(metadata)
        self._metadata[task_id]["updated_at"] = datetime.now().isoformat()
        return True

    def get_history(self, task_id: str) -> List[Dict]:
        """
        Get the state history for a task.
        
        Args:
            task_id: The task identifier
            
        Returns:
            List of state transitions with timestamps
        """
        if task_id in self._metadata:
            return self._metadata[task_id].get("history", [])
        return []

    def list_tasks_by_state(self, state: TaskState) -> List[str]:
        """
        List all task IDs in a specific state.
        
        Args:
            state: The state to filter by
            
        Returns:
            List of task IDs
        """
        return [task_id for task_id, task_state in self._states.items() if task_state == state]

    def get_all_tasks(self) -> Dict[str, TaskState]:
        """
        Get all task states.
        
        Returns:
            Dictionary of task_id to state
        """
        return self._states.copy()

    def delete_task(self, task_id: str) -> bool:
        """
        Delete a task and its metadata.
        
        Args:
            task_id: The task identifier
            
        Returns:
            True if deleted, False if not found
        """
        if task_id in self._states:
            del self._states[task_id]
            if task_id in self._metadata:
                del self._metadata[task_id]
            return True
        return False


state_manager = StateManager()
