import pytest
from unittest.mock import Mock

@pytest.fixture(autouse=True)
def mock_env_vars(monkeypatch):
    """Mock environment variables for testing"""
    monkeypatch.setenv("DEEPSEEK_API_KEY", "test_deepseek_key")
    monkeypatch.setenv("TAVILY_API_KEY", "test_tavily_key")

@pytest.fixture
def mock_client():
    """Create a mock Letta client"""
    client = Mock()
    client.get_archival_memory.return_value = []
    client.insert_archival_memory.return_value = True
    client.create_agent.return_value = Mock(id="test_agent_id")
    return client

@pytest.fixture
def mock_shared_block():
    """Create a mock shared memory block"""
    return Mock(
        id="test_block_id",
        value='{"system_context": {"last_optimization": null}}'
    )