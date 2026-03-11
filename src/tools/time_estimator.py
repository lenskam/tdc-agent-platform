import json
import logging
from typing import Dict, Any
from langchain_core.tools import tool
from ..core.llm_router import llm_router

logger = logging.getLogger(__name__)


class TimeEstimatorTool:
    @tool("estimate_task_duration")
    def estimate_task_duration(task_description: str) -> str:
        """
        Estimates the duration for a task using LLM analysis.
        Returns a JSON object with optimistic, pessimistic, and most_likely estimates in hours.
        
        Args:
            task_description: Description of the task to estimate.
            
        Returns:
            JSON string with estimates: {"optimistic": 4, "pessimistic": 12, "most_likely": 8}
        """
        try:
            model = llm_router.get_model(capability="fast")
            
            prompt = f"""Analyze this task and estimate how long it will take to complete.
Task: {task_description}

Provide a JSON response with three fields:
- optimistic: Best case hours
- pessimistic: Worst case hours  
- most_likely: Most likely hours

Return ONLY valid JSON, no other text."""
            
            response = model.invoke(prompt)
            content = response.content
            
            try:
                result = json.loads(content)
                return json.dumps({
                    "optimistic": result.get("optimistic", 1),
                    "pessimistic": result.get("pessimistic", 8),
                    "most_likely": result.get("most_likely", 4)
                })
            except json.JSONDecodeError:
                import re
                match = re.search(r'\{[^}]+\}', content)
                if match:
                    result = json.loads(match.group())
                    return json.dumps({
                        "optimistic": result.get("optimistic", 1),
                        "pessimistic": result.get("pessimistic", 8),
                        "most_likely": result.get("most_likely", 4)
                    })
                return json.dumps({"optimistic": 1, "pessimistic": 8, "most_likely": 4})
                
        except Exception as e:
            logger.error(f"Time estimation failed: {e}")
            return json.dumps({"optimistic": 1, "pessimistic": 8, "most_likely": 4})


time_estimator_tools = [TimeEstimatorTool.estimate_task_duration]
