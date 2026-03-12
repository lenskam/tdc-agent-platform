from typing import Dict, Optional, Any, Callable
from datetime import datetime
import asyncio
import logging

from .task_router import task_router, TaskRouter
from .state_manager import state_manager, StateManager, TaskState


logger = logging.getLogger(__name__)


class ExecutionResult:
    def __init__(
        self,
        success: bool,
        result: Optional[Any] = None,
        error: Optional[str] = None,
        execution_time: Optional[float] = None
    ):
        self.success = success
        self.result = result
        self.error = error
        self.execution_time = execution_time


class ExecutionEngine:
    def __init__(
        self,
        router: Optional[TaskRouter] = None,
        state_manager: Optional[StateManager] = None
    ):
        self.router = router or task_router
        self.state_manager = state_manager or state_manager
        self._hooks: Dict[str, Callable] = {}

    def register_hook(self, event: str, callback: Callable):
        """
        Register a callback for specific events.
        
        Args:
            event: Event name (e.g., "on_task_start", "on_task_complete")
            callback: Async function to call
        """
        self._hooks[event] = callback

    async def _execute_hook(self, event: str, *args, **kwargs):
        """Execute registered hook if exists."""
        if event in self._hooks:
            hook = self._hooks[event]
            if asyncio.iscoroutinefunction(hook):
                await hook(*args, **kwargs)
            else:
                hook(*args, **kwargs)

    async def execute_task(
        self,
        task_id: str,
        task_type: str,
        task_input: Dict,
        user_id: Optional[str] = None
    ) -> ExecutionResult:
        """
        Execute a task by routing it to the appropriate agent.
        
        Args:
            task_id: Unique identifier for the task
            task_type: The type of task (e.g., "proposal_writing")
            task_input: Input data for the task
            user_id: Optional user who initiated the task
            
        Returns:
            ExecutionResult with success status and output
        """
        start_time = datetime.now()
        
        self.state_manager.create_task(
            task_id=task_id,
            initial_state=TaskState.PENDING,
            metadata={
                "task_type": task_type,
                "user_id": user_id,
                "input": task_input
            }
        )
        
        await self._execute_hook("on_task_start", task_id, task_type, task_input)
        
        try:
            self.state_manager.update_state(task_id, TaskState.QUEUED)
            
            agent_name = self.router.route_task(task_type, task_input)
            
            self.state_manager.update_state(task_id, TaskState.RUNNING)
            self.state_manager.update_metadata(task_id, {
                "agent": agent_name,
                "started_at": datetime.now().isoformat()
            })
            
            logger.info(f"Executing task {task_id} with agent {agent_name}")
            
            agent = self.router.get_agent(agent_name)
            
            if not agent:
                raise ValueError(f"Agent {agent_name} not found")
            
            if hasattr(agent, 'process'):
                result = agent.process(task_input)
            elif hasattr(agent, 'execute'):
                result = agent.execute(task_input)
            elif hasattr(agent, 'run'):
                result = agent.run(task_input)
            else:
                raise ValueError(f"Agent {agent_name} has no executable method")
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            self.state_manager.update_state(task_id, TaskState.COMPLETED)
            self.state_manager.update_metadata(task_id, {
                "completed_at": datetime.now().isoformat(),
                "execution_time": execution_time,
                "result": result if isinstance(result, dict) else {"output": str(result)}
            })
            
            await self._execute_hook("on_task_complete", task_id, result)
            
            return ExecutionResult(
                success=True,
                result=result,
                execution_time=execution_time
            )
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            error_message = str(e)
            
            logger.error(f"Task {task_id} failed: {error_message}")
            
            self.state_manager.update_state(task_id, TaskState.FAILED)
            self.state_manager.update_metadata(task_id, {
                "failed_at": datetime.now().isoformat(),
                "execution_time": execution_time,
                "error": error_message
            })
            
            await self._execute_hook("on_task_error", task_id, error_message)
            
            return ExecutionResult(
                success=False,
                error=error_message,
                execution_time=execution_time
            )

    def execute_task_sync(
        self,
        task_id: str,
        task_type: str,
        task_input: Dict,
        user_id: Optional[str] = None
    ) -> ExecutionResult:
        """
        Synchronous wrapper for execute_task.
        
        Args:
            task_id: Unique identifier for the task
            task_type: The type of task
            task_input: Input data for the task
            user_id: Optional user who initiated the task
            
        Returns:
            ExecutionResult with success status and output
        """
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        return loop.run_until_complete(
            self.execute_task(task_id, task_type, task_input, user_id)
        )

    def get_task_status(self, task_id: str) -> Optional[Dict]:
        """
        Get the current status of a task.
        
        Args:
            task_id: The task identifier
            
        Returns:
            Dictionary with state and metadata, or None if not found
        """
        state = self.state_manager.get_state(task_id)
        if state is None:
            return None
        
        metadata = self.state_manager.get_metadata(task_id) or {}
        return {
            "task_id": task_id,
            "state": state.value,
            "metadata": metadata
        }

    def cancel_task(self, task_id: str) -> bool:
        """
        Cancel a pending or running task.
        
        Args:
            task_id: The task identifier
            
        Returns:
            True if cancelled, False if not found or already completed
        """
        state = self.state_manager.get_state(task_id)
        if state in [TaskState.PENDING, TaskState.QUEUED, TaskState.RUNNING]:
            self.state_manager.update_state(task_id, TaskState.CANCELLED)
            return True
        return False

    def list_tasks(
        self,
        state: Optional[TaskState] = None,
        limit: int = 100
    ) -> list[Dict]:
        """
        List tasks, optionally filtered by state.
        
        Args:
            state: Optional state to filter by
            limit: Maximum number of tasks to return
            
        Returns:
            List of task status dictionaries
        """
        if state:
            task_ids = self.state_manager.list_tasks_by_state(state)
        else:
            task_ids = list(self.state_manager.get_all_tasks().keys())
        
        tasks = []
        for task_id in task_ids[:limit]:
            status = self.get_task_status(task_id)
            if status:
                tasks.append(status)
        
        return tasks


execution_engine = ExecutionEngine()
