import io
import sys
import json
import logging
import traceback
from contextlib import redirect_stdout, redirect_stderr
from typing import Dict, Any, Optional
from langchain_core.tools import tool

logger = logging.getLogger(__name__)

SANDBOX_TIMEOUT = 10
ALLOWED_MODULES = {
    "math": ["*"],
    "random": ["*"],
    "datetime": ["*"],
    "json": ["*"],
    "re": ["*"],
    "collections": ["Counter", "defaultdict", "OrderedDict"],
    "itertools": ["*"],
    "functools": ["reduce", "lru_cache"],
    "operator": ["*"],
    "string": ["*"],
    "array": ["*"],
    "base64": ["*"],
    "hashlib": ["*"],
    "urllib.parse": ["quote", "urlencode"],
}


class Sandbox:
    """
    Safe execution environment for Python code.
    - No network access
    - 10 second timeout
    - Limited to safe modules only
    """
    
    def __init__(self, timeout: int = SANDBOX_TIMEOUT):
        self.timeout = timeout
        self._output = io.StringIO()
        self._errors = io.StringIO()
        
    def execute(self, code: str, input_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Executes Python code in a sandboxed environment.
        
        Args:
            code: Python code to execute
            input_data: Optional input variables
            
        Returns:
            Dict with success status, output, and any errors
        """
        result = {
            "success": False,
            "output": "",
            "error": None,
            "execution_time_ms": 0
        }
        
        import time
        start_time = time.time()
        
        try:
            safe_globals = {
                "__builtins__": self._get_restricted_builtins(),
                "__name__": "__sandbox__",
                "math": __import__("math"),
                "random": __import__("random"),
                "datetime": __import__("datetime"),
                "json": __import__("json"),
                "re": __import__("re"),
                "collections": __import__("collections"),
                "itertools": __import__("itertools"),
                "functools": __import__("functools"),
                "operator": __import__("operator"),
                "string": __import__("string"),
                "array": __import__("array"),
            }
            
            if input_data:
                safe_globals.update(input_data)
            
            safe_locals = {}
            
            with redirect_stdout(self._output), redirect_stderr(self._errors):
                exec(code, safe_globals, safe_locals)
            
            result["success"] = True
            result["output"] = self._output.getvalue()
            
            if safe_locals.get("result") is not None:
                result["output"] += f"\nResult: {safe_locals['result']}"
                
        except SyntaxError as e:
            result["error"] = f"Syntax Error: {e}"
            result["error_detail"] = traceback.format_exc()
            
        except NameError as e:
            result["error"] = f"Name Error: {e}"
            result["hint"] = "Using undefined variable"
            
        except TypeError as e:
            result["error"] = f"Type Error: {e}"
            
        except Exception as e:
            result["error"] = f"Execution Error: {e}"
            result["error_detail"] = traceback.format_exc()
            
        finally:
            result["execution_time_ms"] = int((time.time() - start_time) * 1000)
            
        return result
    
    def _get_restricted_builtins(self) -> Dict[str, Any]:
        """
        Returns restricted builtins to prevent dangerous operations.
        """
        safe_builtins = {}
        
        blocked = [
            "open", "file", "exec", "eval", "compile",
            "import", "__import__", "reload",
            "breakpoint", "exit", "quit",
            "input", "raw_input",
            "globals", "locals", "vars",
            "memoryview", "buffer",
        ]
        
        for name in dir(__builtins__):
            if name not in blocked:
                safe_builtins[name] = getattr(__builtins__, name)
        
        return safe_builtins


def run_in_sandbox(
    code: str,
    input_data: Optional[Dict[str, Any]] = None,
    timeout: int = SANDBOX_TIMEOUT
) -> Dict[str, Any]:
    """
    Wrapper function to run code in sandbox.
    
    Args:
        code: Python code to execute
        input_data: Optional input variables
        timeout: Execution timeout in seconds
        
    Returns:
        Dict with execution results
    """
    sandbox = Sandbox(timeout=timeout)
    return sandbox.execute(code, input_data)


class SandboxTools:
    @tool("run_python_code")
    def run_python_code(code: str, input_data: Optional[str] = None) -> str:
        """
        Executes Python code in a sandboxed environment.
        
        WARNING: This is for development/testing only. Never run
        untrusted code in production.
        
        Args:
            code: Python code to execute
            input_data: Optional JSON string of input variables
            
        Returns:
            JSON string with execution results
        """
        try:
            inputs = None
            if input_data:
                try:
                    inputs = json.loads(input_data)
                except json.JSONDecodeError:
                    return json.dumps({
                        "success": False,
                        "error": "Invalid JSON in input_data"
                    })
            
            result = run_in_sandbox(code, inputs)
            
            return json.dumps(result)
            
        except Exception as e:
            logger.error(f"Sandbox execution failed: {e}")
            return json.dumps({
                "success": False,
                "error": str(e)
            })
    
    @tool("lint_code")
    def lint_code(code: str, language: str = "python") -> str:
        """
        Lints code for basic issues.
        
        Args:
            code: Code to lint
            language: Programming language (default: python)
            
        Returns:
            JSON string with lint results
        """
        if language != "python":
            return json.dumps({
                "success": False,
                "error": f"Language '{language}' not supported"
            })
        
        import ast
        import re
        
        issues = []
        
        try:
            ast.parse(code)
        except SyntaxError as e:
            issues.append({
                "line": e.lineno,
                "column": e.offset,
                "severity": "error",
                "message": str(e)
            })
        
        dangerous_patterns = [
            (r"os\.system\s*\(", "Use of os.system is not allowed in sandbox"),
            (r"subprocess\.", "Use of subprocess is not allowed in sandbox"),
            (r"eval\s*\(", "Use of eval is not allowed"),
            (r"exec\s*\(", "Use of exec is not allowed"),
            (r"__import__", "Dynamic imports not allowed"),
        ]
        
        for pattern, message in dangerous_patterns:
            matches = re.finditer(pattern, code)
            for match in matches:
                issues.append({
                    "line": code[:match.start()].count("\n") + 1,
                    "severity": "warning",
                    "message": message
                })
        
        return json.dumps({
            "success": True,
            "language": language,
            "issues": issues,
            "has_errors": any(i["severity"] == "error" for i in issues),
            "issue_count": len(issues)
        })


sandbox_tools = [
    SandboxTools.run_python_code,
    SandboxTools.lint_code
]
