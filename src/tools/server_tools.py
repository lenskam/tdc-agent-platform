import os
import json
import logging
import subprocess
from typing import Optional, List, Dict, Any
from langchain_core.tools import tool

logger = logging.getLogger(__name__)

ALLOWED_DOCKER_CONTAINERS = os.getenv("ALLOWED_DOCKER_CONTAINERS", "").split(",")
LOG_DIR = os.getenv("LOG_DIR", "/var/log")


class ServerTools:
    @tool("get_system_metrics")
    def get_system_metrics() -> str:
        """
        Gets current system metrics (CPU, Memory, Disk usage).

        Returns:
            JSON string with system metrics
        """
        try:
            import psutil
            
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            return json.dumps({
                "success": True,
                "cpu": {
                    "percent": cpu_percent,
                    "count": psutil.cpu_count()
                },
                "memory": {
                    "total_gb": round(memory.total / (1024**3), 2),
                    "available_gb": round(memory.available / (1024**3), 2),
                    "used_gb": round(memory.used / (1024**3), 2),
                    "percent": memory.percent
                },
                "disk": {
                    "total_gb": round(disk.total / (1024**3), 2),
                    "used_gb": round(disk.used / (1024**3), 2),
                    "free_gb": round(disk.free / (1024**3), 2),
                    "percent": disk.percent
                }
            })
            
        except ImportError:
            return json.dumps({
                "success": False,
                "error": "psutil not installed. Run: pip install psutil"
            })
        except Exception as e:
            logger.error(f"Failed to get system metrics: {e}")
            return json.dumps({
                "success": False,
                "error": str(e)
            })

    @tool("list_docker_containers")
    def list_docker_containers(all_containers: bool = True) -> str:
        """
        Lists Docker containers.

        Args:
            all_containers: Include stopped containers (default: True)

        Returns:
            JSON string with container list
        """
        try:
            cmd = ["docker", "ps", "--format", "{{json . }}"]
            if all_containers:
                cmd.append("-a")
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            containers = []
            for line in result.stdout.strip().split("\n"):
                if line:
                    containers.append(json.loads(line))
            
            if ALLOWED_DOCKER_CONTAINERS and ALLOWED_DOCKER_CONTAINERS[0]:
                containers = [
                    c for c in containers 
                    if c.get("Names") in ALLOWED_DOCKER_CONTAINERS
                ]
            
            return json.dumps({
                "success": True,
                "containers": containers,
                "count": len(containers)
            })
            
        except FileNotFoundError:
            return json.dumps({
                "success": False,
                "error": "Docker not available"
            })
        except subprocess.CalledProcessError as e:
            return json.dumps({
                "success": False,
                "error": str(e)
            })

    @tool("get_container_logs")
    def get_container_logs(
        container_name: str,
        lines: int = 50,
        since: Optional[str] = None
    ) -> str:
        """
        Gets logs from a Docker container (READ ONLY).

        Args:
            container_name: Name of the container
            lines: Number of lines to fetch (default: 50)
            since: Optional time filter (e.g., "1h", "30m")

        Returns:
            JSON string with container logs
        """
        try:
            if ALLOWED_DOCKER_CONTAINERS and ALLOWED_DOCKER_CONTAINERS[0]:
                if container_name not in ALLOWED_DOCKER_CONTAINERS:
                    return json.dumps({
                        "success": False,
                        "error": f"Container '{container_name}' not in allowed list"
                    })
            
            cmd = ["docker", "logs", "--tail", str(lines), container_name]
            
            if since:
                cmd.extend(["--since", since])
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            output = result.stdout + result.stderr
            
            error_lines = [l for l in output.split("\n") if "error" in l.lower() or "exception" in l.lower()]
            
            return json.dumps({
                "success": True,
                "container": container_name,
                "lines": lines,
                "log_preview": output[:5000],
                "error_count": len(error_lines),
                "errors": error_lines[:5]
            })
            
        except subprocess.TimeoutExpired:
            return json.dumps({
                "success": False,
                "error": "Log retrieval timed out"
            })
        except Exception as e:
            return json.dumps({
                "success": False,
                "error": str(e)
            })

    @tool("tail_logs")
    def tail_logs(log_path: str, lines: int = 100) -> str:
        """
        Reads the last lines of a log file.

        Args:
            log_path: Path to the log file
            lines: Number of lines to read (default: 100)

        Returns:
            JSON string with log content
        """
        try:
            safe_paths = [LOG_DIR, "/app/logs", "./logs"]
            
            is_safe = any(log_path.startswith(p) for p in safe_paths if os.path.exists(p))
            
            if not is_safe:
                return json.dumps({
                    "success": False,
                    "error": f"Path not in allowed directories: {safe_paths}"
                })
            
            if not os.path.exists(log_path):
                return json.dumps({
                    "success": False,
                    "error": f"File not found: {log_path}"
                })
            
            with open(log_path, "r") as f:
                all_lines = f.readlines()
                last_lines = all_lines[-lines:]
            
            return json.dumps({
                "success": True,
                "file": log_path,
                "lines": len(last_lines),
                "content": "".join(last_lines)
            })
            
        except PermissionError:
            return json.dumps({
                "success": False,
                "error": "Permission denied"
            })
        except Exception as e:
            return json.dumps({
                "success": False,
                "error": str(e)
            })

    @tool("deploy_service")
    def deploy_service(service_name: str, action: str = "status") -> str:
        """
        Manages service deployment (READ-ONLY operations by default).

        Args:
            service_name: Name of the service
            action: Action to perform (status, restart, stop) - status is default and read-only

        Returns:
            JSON string with deployment status
        """
        if action not in ["status", "restart", "stop"]:
            return json.dumps({
                "success": False,
                "error": f"Invalid action: {action}. Allowed: status"
            })
        
        if action in ["restart", "stop"]:
            return json.dumps({
                "success": False,
                "error": "Write operations require human approval. Use 'status' for read-only.",
                "note": "DevOps agent has read-only access initially"
            })
        
        try:
            result = subprocess.run(
                ["docker", "ps", "--filter", f"name={service_name}", "--format", "{{json . }}"],
                capture_output=True,
                text=True,
                check=True
            )
            
            containers = []
            for line in result.stdout.strip().split("\n"):
                if line:
                    containers.append(json.loads(line))
            
            if not containers:
                return json.dumps({
                    "success": True,
                    "service": service_name,
                    "status": "not_found",
                    "message": f"No container found for service '{service_name}'"
                })
            
            return json.dumps({
                "success": True,
                "service": service_name,
                "status": "running",
                "containers": containers
            })
            
        except Exception as e:
            return json.dumps({
                "success": False,
                "error": str(e)
            })

    @tool("check_api_health")
    def check_api_health(url: str = "http://localhost:8000/health") -> str:
        """
        Checks the health of an API endpoint.

        Args:
            url: URL to check (default: localhost:8000/health)

        Returns:
            JSON string with health status
        """
        try:
            import requests
            
            response = requests.get(url, timeout=5)
            
            return json.dumps({
                "success": True,
                "url": url,
                "status_code": response.status_code,
                "response_time_ms": int(response.elapsed.total_seconds() * 1000),
                "is_healthy": response.status_code == 200
            })
            
        except ImportError:
            return json.dumps({
                "success": False,
                "error": "requests not installed"
            })
        except Exception as e:
            return json.dumps({
                "success": False,
                "url": url,
                "error": str(e),
                "is_healthy": False
            })


server_tools = [
    ServerTools.get_system_metrics,
    ServerTools.list_docker_containers,
    ServerTools.get_container_logs,
    ServerTools.tail_logs,
    ServerTools.deploy_service,
    ServerTools.check_api_health
]
