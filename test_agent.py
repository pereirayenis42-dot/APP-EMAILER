# test_agent.py
import pytest

# Dummy agent function for demonstration
def simple_agent(prompt):
    if not prompt:
        return "Please provide a prompt."
    return f"Processed: {prompt}"

# Test case 1: Standard input
def test_agent_response():
    response = simple_agent("Hello")
    assert response == "Processed: Hello"

# Test case 2: Edge case (empty input)
def test_agent_empty_input():
    response = simple_agent("")
    assert response == "Please provide a prompt."
