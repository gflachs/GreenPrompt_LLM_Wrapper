import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from src.app.main import app, wrapper
from src.app.models.request import ModelConfig, PromptingArgs, DeploymentArgs, ModelArgs

client = TestClient(app)

@pytest.fixture(autouse=True)
def run_around_tests():
    global wrapper
    wrapper = None
    yield
    wrapper = None

def test_get_status_idle():
    """Tests whether the status `idle` is returned if no wrapper is provided."""
    response = client.get("/get_status")
    assert response.status_code == 200
    assert response.json() == {"status": "success", "message": "idle"}

def test_process_prompt_without_wrapper():
    """Tests whether `process_prompt` responds correctly if no wrapper is provided."""
    global wrapper
    wrapper = None  # Simulate missing wrapper
    
    prompt_data = {"question": "What is the meaning of life?"}
    expected_response = {
        "answer": "The wrapper is not available",
        "sci_score": 0
    }
    
    response = client.post("/process_prompt", json=prompt_data)
    assert response.status_code == 200
    assert response.json() == expected_response

def test_deploy():
    """Tests whether `deploy` responds correctly when a wrapper is successfully deployed."""
    config_data = {
        "model": "test-model",
        "modeltyp": "test-type",
        "args": {
            "prompting": {},
            "deployment": {}
        },
        "uses_chat_template": False
    }
    
    # Mock WrapperManager to avoid actual model download
    with patch('src.app.main.WrapperManager') as MockWrapperManager:
        mock_wrapper_manager = MockWrapperManager.return_value
        mock_wrapper = MagicMock()
        mock_wrapper.llm.status = "ready"
        mock_wrapper_manager.create_wrapper.return_value = mock_wrapper
        
        response = client.post("/deploy", json=config_data)
        assert response.status_code == 200
        assert response.json() == {
            "status": "success",
            "message": "The Wrapper succesfully deployed the model test-model"
        }

def test_deploy_with_existing_wrapper():
    """Tests whether `deploy` responds correctly if a wrapper is already deployed."""
    global wrapper
    wrapper = MagicMock()
    wrapper.llm.model = "existing-model"
    
    config_data = {
        "model": "new-model",
        "modeltyp": "test-type",
        "args": {
            "prompting": {},
            "deployment": {}
        },
        "uses_chat_template": False
    }
    
    with patch('src.app.main.WrapperManager') as MockWrapperManager:
        mock_wrapper_manager = MockWrapperManager.return_value
        mock_wrapper_manager.create_wrapper.return_value = wrapper
        
        response = client.post("/deploy", json=config_data)
        
        expected_message = "Unable to deploy the model new-model, because there is already a model deployed."
        
        assert response.status_code == 200
        assert response.json() == {
            "status": "failure",
            "message": expected_message
        }

