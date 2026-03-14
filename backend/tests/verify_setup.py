import sys
import os
from unittest.mock import MagicMock, patch

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def test_imports():
    print("Testing imports...")
    try:
        from src.core.llm_router import LLMRouter
        from src.database.postgres import Base, engine
        from src.agents.pm_agent import ProjectManagerAgent
        from src.api.main import app
        print("✅ Critical imports successful.")
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        sys.exit(1)

def test_agent_init():
    print("Testing PM Agent Initialization (Mocked)...")
    # Mock environment variables
    with patch.dict(os.environ, {"OPENAI_API_KEY": "sk-test-key", "DEFAULT_LLM_PROVIDER": "openai"}):
         with patch("src.agents.base_agent.BaseTDCAgent") as MockBase:
             # Just checking if we can instantiate class without syntax errors
             try:
                 from src.agents.pm_agent import ProjectManagerAgent
                 agent = ProjectManagerAgent()
                 print("✅ ProjectManagerAgent instantiated.")
             except Exception as e:
                 print(f"❌ Agent init failed: {e}")

if __name__ == "__main__":
    test_imports()
    test_agent_init()
