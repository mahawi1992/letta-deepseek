import pytest
from datetime import datetime
from unittest.mock import Mock
from components.documentation import EnhancedDocumentation

@pytest.fixture
def mock_client():
    return Mock()

@pytest.fixture
def doc_system(mock_client):
    return EnhancedDocumentation(mock_client, "test_agent_id")

@pytest.fixture
def sample_content():
    return {
        "code": "def test(): pass",
        "explanation": "Test function",
        "language": "python",
        "complexity": "low"
    }

async def test_store_documentation(doc_system, sample_content):
    # Test storing documentation
    doc_type = "code_snippet"
    metadata = {"category": "testing"}
    
    await doc_system.store_documentation(doc_type, sample_content, metadata)
    
    # Verify client call
    doc_system.client.insert_archival_memory.assert_called_once()
    call_args = doc_system.client.insert_archival_memory.call_args[0]
    
    assert call_args[0] == "test_agent_id"
    assert "DOCUMENTATION_code_snippet" in call_args[1]

async def test_search_documentation(doc_system):
    # Mock archival memory
    mock_memory = [
        Mock(text="DOCUMENTATION_test: " + '{"content": {"test": true}, "metadata": {"category": "testing"}}')
    ]
    doc_system.client.get_archival_memory.return_value = mock_memory
    
    # Test search
    results = await doc_system.search_documentation("test", {"category": "testing"})
    
    assert len(results) == 1
    assert results[0]["content"]["test"] is True

def test_extract_keywords(doc_system, sample_content):
    keywords = doc_system._extract_keywords(sample_content)
    assert "function" in keywords
    assert "python" in keywords

def test_categorize_content(doc_system):
    # Test implementation category
    impl_content = {"content": "def implement_feature(): pass"}
    assert doc_system._categorize_content(impl_content) == "implementation"
    
    # Test security category
    sec_content = {"content": "authentication and encryption"}
    assert doc_system._categorize_content(sec_content) == "security"

def test_detect_language(doc_system):
    # Test Python detection
    py_content = {"content": "def test(): pass"}
    assert doc_system._detect_language(py_content) == "python"
    
    # Test JavaScript detection
    js_content = {"content": "function test() {}"}
    assert doc_system._detect_language(js_content) == "javascript"

def test_assess_complexity(doc_system):
    # Test high complexity
    high_content = {"content": "advanced distributed system optimization"}
    assert doc_system._assess_complexity(high_content) == "high"
    
    # Test low complexity
    low_content = {"content": "basic introduction to programming"}
    assert doc_system._assess_complexity(low_content) == "low"

def test_matches_filters(doc_system):
    doc = {
        "metadata": {
            "category": "testing",
            "language": "python",
            "complexity": "low"
        }
    }
    
    # Test matching filter
    assert doc_system._matches_filters(doc, {"category": "testing"}) is True
    
    # Test non-matching filter
    assert doc_system._matches_filters(doc, {"category": "security"}) is False
    
    # Test multiple filters
    assert doc_system._matches_filters(
        doc,
        {"category": "testing", "language": "python"}
    ) is True