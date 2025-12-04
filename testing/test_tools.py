"""
Testing Tools and Function Calling

Tests for agent tools and function calling capabilities.
"""

import pytest
import json
from typing import Dict, Any


def calculator(expression: str) -> float:
    """Simple calculator tool"""
    try:
        return eval(expression, {"__builtins__": {}}, {})
    except Exception as e:
        raise ValueError(f"Invalid expression: {e}")


def weather_tool(location: str) -> Dict[str, Any]:
    """Mock weather tool"""
    weather_db = {
        "Tokyo": {"temp": 22, "condition": "sunny"},
        "London": {"temp": 15, "condition": "rainy"},
        "New York": {"temp": 18, "condition": "cloudy"}
    }
    return weather_db.get(location, {"temp": 20, "condition": "unknown"})


class TestCalculatorTool:
    """Tests for calculator tool"""
    
    def test_addition(self):
        assert calculator("2 + 2") == 4
    
    def test_multiplication(self):
        assert calculator("5 * 10") == 50
    
    def test_complex_expression(self):
        assert calculator("(10 + 5) * 2") == 30
    
    def test_invalid_expression(self):
        with pytest.raises(ValueError):
            calculator("invalid")
    
    def test_division_by_zero(self):
        with pytest.raises(ZeroDivisionError):
            calculator("10 / 0")


class TestWeatherTool:
    """Tests for weather tool"""
    
    def test_known_location(self):
        result = weather_tool("Tokyo")
        assert result["temp"] == 22
        assert result["condition"] == "sunny"
    
    def test_unknown_location(self):
        result = weather_tool("Unknown City")
        assert result["condition"] == "unknown"
    
    def test_multiple_locations(self):
        locations = ["Tokyo", "London", "New York"]
        for loc in locations:
            result = weather_tool(loc)
            assert "temp" in result
            assert "condition" in result


class TestToolIntegration:
    """Tests for tool integration with agents"""
    
    def test_tool_definition_format(self):
        """Test tool is properly formatted for OpenAI"""
        tool_def = {
            "type": "function",
            "function": {
                "name": "calculator",
                "description": "Perform calculations",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "expression": {"type": "string"}
                    },
                    "required": ["expression"]
                }
            }
        }
        
        assert tool_def["type"] == "function"
        assert "name" in tool_def["function"]
        assert "parameters" in tool_def["function"]
    
    def test_tool_response_format(self):
        """Test tool returns proper format"""
        result = weather_tool("Tokyo")
        assert isinstance(result, dict)
        assert all(key in result for key in ["temp", "condition"])
    
    def test_multiple_tool_calls(self):
        """Test executing multiple tools in sequence"""
        # Simulate tool call sequence
        calc_result = calculator("5 + 5")
        weather_result = weather_tool("Tokyo")
        
        assert calc_result == 10
        assert weather_result["temp"] == 22


def test_tool_error_handling():
    """Test tools handle errors properly"""
    
    # Test calculator error
    try:
        calculator("1 / 0")
        assert False
    except ZeroDivisionError:
        pass
    
    # Test weather tool with invalid input
    result = weather_tool("")
    assert result["condition"] == "unknown"


@pytest.fixture
def mock_tool_response():
    """Fixture providing mock tool response"""
    return {
        "tool_call_id": "call_123",
        "role": "tool",
        "name": "calculator",
        "content": json.dumps({"result": 42})
    }


def test_tool_response_parsing(mock_tool_response):
    """Test parsing tool responses"""
    assert mock_tool_response["role"] == "tool"
    content = json.loads(mock_tool_response["content"])
    assert content["result"] == 42


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
