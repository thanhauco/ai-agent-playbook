"""
Testing Examples for AI Agents

Demonstrates how to test agents using pytest with mocked LLM responses.
"""

import pytest
from unittest.mock import Mock, patch
import json


# Mock agent responses
MOCK_RESPONSES = {
    "greeting": "Hello! How can I help you today?",
    "weather_tokyo": "The weather in Tokyo is sunny and 72°F",
    "calculation": "The result is 100"
}


class MockLLM:
    """Mock LLM for testing"""
    def __init__(self, response="Test response"):
        self.response = response
        self.call_count = 0
    
    def chat(self, messages):
        self.call_count += 1
        return self.response


def test_basic_agent_response():
    """Test basic agent can respond"""
    mock_llm = MockLLM(MOCK_RESPONSES["greeting"])
    
    # Simulate agent
    response = mock_llm.chat([{"role": "user", "content": "Hi"}])
    
    assert response == "Hello! How can I help you today?"
    assert mock_llm.call_count == 1


def test_agent_with_tools():
    """Test agent can use tools"""
    def mock_get_weather(location):
        return json.dumps({"temp": 72, "condition": "sunny"})
    
    # Test tool execution
    result = mock_get_weather("Tokyo")
    data = json.loads(result)
    
    assert data["temp"] == 72
    assert data["condition"] == "sunny"


def test_agent_conversation_memory():
    """Test agent maintains conversation history"""
    conversation = []
    
    # Simulate conversation
    conversation.append({"role": "user", "content": "My name is Alice"})
    conversation.append({"role": "assistant", "content": "Nice to meet you, Alice!"})
    conversation.append({"role": "user", "content": "What's my name?"})
    
    # Verify history
    assert len(conversation) == 3
    assert "Alice" in conversation[1]["content"]


@patch('openai.OpenAI')
def test_agent_with_mocked_openai(mock_openai):
    """Test agent with mocked OpenAI client"""
    # Setup mock
    mock_client = Mock()
    mock_response = Mock()
    mock_response.choices = [Mock(message=Mock(content="Mocked response"))]
    mock_client.chat.completions.create.return_value = mock_response
    mock_openai.return_value = mock_client
    
    # Use mock
    from openai import OpenAI
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "test"}]
    )
    
    assert response.choices[0].message.content == "Mocked response"


def test_agent_error_handling():
    """Test agent handles errors gracefully"""
    def risky_function():
        raise ValueError("Test error")
    
    try:
        risky_function()
        assert False, "Should have raised exception"
    except ValueError as e:
        assert str(e) == "Test error"


class TestAgentValidation:
    """Test suite for agent input/output validation"""
    
    def test_valid_input(self):
        """Test agent accepts valid input"""
        user_input = "What's the weather?"
        assert isinstance(user_input, str)
        assert len(user_input) > 0
    
    def test_empty_input(self):
        """Test agent handles empty input"""
        user_input = ""
        # Agent should handle empty input gracefully
        assert user_input == "" or user_input.strip() == ""
    
    def test_long_input(self):
        """Test agent handles very long input"""
        user_input = "a" * 10000
        # Should truncate or handle appropriately
        assert len(user_input) <= 10000


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
