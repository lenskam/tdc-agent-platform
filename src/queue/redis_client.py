import os
import json
from typing import Optional, Dict, Any, List
import redis
import logging


logger = logging.getLogger(__name__)


class RedisClient:
    def __init__(self):
        self.host = os.getenv("REDIS_HOST", "localhost")
        self.port = int(os.getenv("REDIS_PORT", "6379"))
        self.db = int(os.getenv("REDIS_DB", "0"))
        self.password = os.getenv("REDIS_PASSWORD")
        self._client: Optional[redis.Redis] = None

    @property
    def client(self) -> redis.Redis:
        if self._client is None:
            self._client = redis.Redis(
                host=self.host,
                port=self.port,
                db=self.db,
                password=self.password,
                decode_responses=True
            )
        return self._client

    def ping(self) -> bool:
        try:
            return self.client.ping()
        except Exception as e:
            logger.error(f"Redis ping failed: {e}")
            return False

    def enqueue_task(self, queue_name: str, task_data: Dict[str, Any]) -> str:
        """
        Add a task to the queue.
        
        Args:
            queue_name: Name of the queue
            task_data: Task data to enqueue
            
        Returns:
            Task ID
        """
        task_id = task_data.get("task_id", f"{queue_name}:{self.client.incr('task_counter')}")
        task_data["task_id"] = task_id
        
        self.client.rpush(queue_name, json.dumps(task_data))
        logger.info(f"Enqueued task {task_id} to {queue_name}")
        
        return task_id

    def dequeue_task(self, queue_name: str, timeout: int = 0) -> Optional[Dict[str, Any]]:
        """
        Get a task from the queue.
        
        Args:
            queue_name: Name of the queue
            timeout: Blocking timeout in seconds (0 = non-blocking)
            
        Returns:
            Task data or None if queue is empty
        """
        if timeout > 0:
            result = self.client.blpop(queue_name, timeout=timeout)
            if result:
                _, task_json = result
                return json.loads(task_json)
        else:
            result = self.client.lpop(queue_name)
            if result:
                return json.loads(result)
        
        return None

    def get_queue_length(self, queue_name: str) -> int:
        """
        Get the length of a queue.
        
        Args:
            queue_name: Name of the queue
            
        Returns:
            Number of items in queue
        """
        return self.client.llen(queue_name)

    def list_queues(self) -> List[str]:
        """
        List all queue keys.
        
        Returns:
            List of queue names
        """
        return [k for k in self.client.keys("*") if self.client.type(k) == "list"]

    def set_task_status(self, task_id: str, status: str, result: Optional[Dict] = None):
        """
        Set task status in Redis.
        
        Args:
            task_id: Unique task identifier
            status: Status string
            result: Optional result data
        """
        key = f"task_status:{task_id}"
        data = {"status": status}
        if result:
            data["result"] = result
        
        self.client.setex(key, 86400, json.dumps(data))  # 24 hour TTL

    def get_task_status(self, task_id: str) -> Optional[Dict]:
        """
        Get task status from Redis.
        
        Args:
            task_id: Unique task identifier
            
        Returns:
            Status data or None
        """
        key = f"task_status:{task_id}"
        data = self.client.get(key)
        if data:
            return json.loads(data)
        return None

    def publish_event(self, channel: str, message: Dict[str, Any]):
        """
        Publish an event to a channel.
        
        Args:
            channel: Channel name
            message: Message to publish
        """
        self.client.publish(channel, json.dumps(message))

    def subscribe(self, channel: str):
        """
        Subscribe to a channel.
        
        Args:
            channel: Channel name
            
        Returns:
            PubSub object
        """
        return self.client.pubsub()


redis_client = RedisClient()
