import asyncio
import logging
from typing import Optional, Callable, Dict, Any
import signal
import sys

from .redis_client import RedisClient, redis_client
from ..orchestrator.execution_engine import ExecutionEngine


logger = logging.getLogger(__name__)


class TaskWorker:
    def __init__(
        self,
        queue_name: str = "task_queue",
        redis_client: Optional[RedisClient] = None,
        execution_engine: Optional[ExecutionEngine] = None
    ):
        self.queue_name = queue_name
        self.redis = redis_client or redis_client
        self.execution_engine = execution_engine or ExecutionEngine()
        self.is_running = False
        self._task_handlers: Dict[str, Callable] = {}

    def register_handler(self, task_type: str, handler: Callable):
        """
        Register a custom handler for a specific task type.
        
        Args:
            task_type: Type of task
            handler: Async function to handle the task
        """
        self._task_handlers[task_type] = handler
        logger.info(f"Registered handler for task type: {task_type}")

    async def process_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a single task.
        
        Args:
            task_data: Task data including task_id, task_type, and input
            
        Returns:
            Result dictionary
        """
        task_id = task_data.get("task_id")
        task_type = task_data.get("task_type")
        task_input = task_data.get("input", {})
        user_id = task_data.get("user_id")
        
        logger.info(f"Processing task {task_id} of type {task_type}")
        
        if task_type in self._task_handlers:
            handler = self._task_handlers[task_type]
            result = await handler(task_input)
        else:
            result = await self.execution_engine.execute_task(
                task_id=task_id,
                task_type=task_type,
                task_input=task_input,
                user_id=user_id
            )
            
            result = {
                "success": result.success,
                "result": result.result,
                "error": result.error
            }
        
        return result

    async def run(self, poll_interval: float = 1.0):
        """
        Run the worker loop.
        
        Args:
            poll_interval: How often to poll for new tasks (seconds)
        """
        self.is_running = True
        
        logger.info(f"Worker started, listening on queue: {self.queue_name}")
        
        while self.is_running:
            try:
                task_data = self.redis.dequeue_task(self.queue_name, timeout=int(poll_interval))
                
                if task_data:
                    task_id = task_data.get("task_id", "unknown")
                    self.redis.set_task_status(task_id, "running")
                    
                    try:
                        result = await self.process_task(task_data)
                        
                        if result.get("success"):
                            self.redis.set_task_status(task_id, "completed", result)
                        else:
                            self.redis.set_task_status(task_id, "failed", result)
                            
                    except Exception as e:
                        logger.error(f"Error processing task {task_id}: {e}")
                        self.redis.set_task_status(task_id, "failed", {"error": str(e)})
                
                await asyncio.sleep(0.1)
                
            except Exception as e:
                logger.error(f"Worker error: {e}")
                await asyncio.sleep(poll_interval)
        
        logger.info("Worker stopped")

    def stop(self):
        """Stop the worker."""
        self.is_running = False
        logger.info("Stopping worker...")


def create_worker(
    queue_name: str = "task_queue",
    additional_handlers: Optional[Dict[str, Callable]] = None
) -> TaskWorker:
    """
    Create and configure a task worker.
    
    Args:
        queue_name: Name of the queue to listen to
        additional_handlers: Optional dict of custom task handlers
        
    Returns:
        Configured TaskWorker instance
    """
    worker = TaskWorker(queue_name=queue_name)
    
    if additional_handlers:
        for task_type, handler in additional_handlers.items():
            worker.register_handler(task_type, handler)
    
    return worker


def run_worker_cli():
    """CLI entry point for running the worker."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Run task queue worker")
    parser.add_argument("--queue", default="task_queue", help="Queue name to process")
    args = parser.parse_args()
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    worker = TaskWorker(queue_name=args.queue)
    
    def signal_handler(sig, frame):
        worker.stop()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    asyncio.run(worker.run())


if __name__ == "__main__":
    run_worker_cli()
