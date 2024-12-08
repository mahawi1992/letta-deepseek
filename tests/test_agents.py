import pytest
from unittest.mock import Mock, patch
from components.agents import ResearchAgent, CodingAgent
from components.documentation import EnhancedDocumentation

@pytest.fixture
def mock_client():
    return Mock()

@pytest.fixture
def mock_shared_block():
    return Mock()

@pytest.fixture
def research_agent(mock_client, mock_shared_block):
    return ResearchAgent(
        mock_client,
        mock_shared_block,
        enhanced_features={'documentation_storage': True}
    )

@pytest.fixture
def coding_agent(mock_client, mock_shared_block):
    return CodingAgent(mock_client, mock_shared_block)

async def test_research_agent_initialization(research_agent):
    assert research_agent.client is not None
    assert research_agent.shared_block is not None
    assert hasattr(research_agent, 'docs')
    assert isinstance(research_agent.docs, EnhancedDocumentation)

async def test_research_with_existing_documentation(research_agent):
    # Mock documentation search
    existing_docs = [{
        'metadata': {
            'timestamp': '2024-01-01T00:00:00',
            'query': 'test query'
        },
        'content': {
            'summary': 'test summary',
            'results': []
        }
    }]
    research_agent.docs.search_documentation = Mock(return_value=existing_docs)
    
    result = await research_agent.research('test query')
    assert result['source'] == 'documentation'
    assert result['summary'] == 'test summary'

async def test_research_with_tavily_search(research_agent):
    # Mock empty documentation search
    research_agent.docs.search_documentation = Mock(return_value=[])
    
    # Mock Tavily search results
    mock_search_results = [{'title': 'Test', 'content': 'Test content'}]
    research_agent.search_tool.run = Mock(return_value=mock_search_results)
    
    # Mock client response
    mock_response = Mock()
    mock_response.messages = [Mock(content='Analysis summary')]
    research_agent.client.send_message = Mock(return_value=mock_response)
    
    result = await research_agent.research('test query')
    assert 'summary' in result
    assert result['results'] == mock_search_results

async def test_coding_agent_implementation(coding_agent):
    # Mock research findings
    research_findings = {
        'summary': 'Test findings',
        'best_practices': ['Practice 1', 'Practice 2']
    }
    
    # Mock client response
    mock_response = Mock()
    mock_response.messages = [Mock(
        content='Explanation\n```python\ndef test():\n    pass\n```'
    )]
    coding_agent.client.send_message = Mock(return_value=mock_response)
    
    result = await coding_agent.implement(research_findings, 'test request')
    assert 'explanation' in result
    assert 'code' in result
    assert result['research_findings'] == research_findings

async def test_coding_agent_error_handling(coding_agent):
    with pytest.raises(Exception):
        await coding_agent.implement(None, 'test request')

async def test_research_agent_categories(research_agent):
    text = 'This involves security authentication and performance optimization'
    categories = research_agent._extract_categories(text)
    assert 'security' in categories
    assert 'performance' in categories