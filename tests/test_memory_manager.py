import pytest
from datetime import datetime
from unittest.mock import Mock, patch
from components.memory_manager import MemoryOptimizer

@pytest.fixture
def mock_client():
    return Mock()

@pytest.fixture
def memory_optimizer(mock_client):
    return MemoryOptimizer(mock_client, "test_agent_id")

@pytest.fixture
def sample_memories():
    return [
        Mock(text="DOCUMENTATION_code: " + '{"type": "code", "content": {"test": true}, "timestamp": "2024-01-01T00:00:00"}'),
        Mock(text="DOCUMENTATION_code: " + '{"type": "code", "content": {"test": true}, "timestamp": "2024-01-02T00:00:00"}')
    ]

async def test_consolidate_memory(memory_optimizer, sample_memories):
    memory_optimizer.client.get_archival_memory.return_value = sample_memories
    await memory_optimizer.consolidate_similar_memories()
    
    # Verify merged memory was stored
    memory_optimizer.client.insert_archival_memory.assert_called_once()

async def test_cleanup_old_memories(memory_optimizer):
    old_memory = Mock(
        text="DOCUMENTATION_test: " + '{"timestamp": "2023-01-01T00:00:00", "importance": 0.1}'
    )
    memory_optimizer.client.get_archival_memory.return_value = [old_memory]
    
    await memory_optimizer.cleanup_old_memories()
    memory_optimizer.client.delete_archival_memory.assert_called_once()

def test_is_memory_important(memory_optimizer):
    # Test important memory
    important_memory = {
        "access_count": 100,
        "success_rate": 0.95,
        "relevance": 0.9
    }
    assert memory_optimizer._is_memory_important(important_memory) is True
    
    # Test unimportant memory
    unimportant_memory = {
        "access_count": 1,
        "success_rate": 0.1,
        "relevance": 0.2
    }
    assert memory_optimizer._is_memory_important(unimportant_memory) is False

async def test_optimize_memory_structure(memory_optimizer):
    with patch('components.memory_manager.MemoryOptimizer._update_memory_indices') as mock_update:
        await memory_optimizer.optimize_memory_structure()
        mock_update.assert_called_once()

@pytest.mark.parametrize("input_version,expected", [
    ("1.0", "1.1"),
    ("2.5", "2.6"),
    ("invalid", "1.1")
])
def test_increment_version(memory_optimizer, input_version, expected):
    result = memory_optimizer._increment_version(input_version)
    assert result == expected