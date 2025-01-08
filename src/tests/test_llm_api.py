from fastapi.testclient import TestClient
from src.app.llm_api import app

client = TestClient(app)

def test_deploy_model():
    response = client.post("/deploy", json={"model_type": "text-generation", "model_name": "TinyLlama/TinyLlama-1.1B-Chat-v1.0"})
    assert response.status_code == 200
    assert response.json()["message"] == "Model deployed successfully"

def test_prompt_with_valid_question():
    
    client.post("/deploy", json={"model_type": "text-generation", "model_name": "TinyLlama/TinyLlama-1.1B-Chat-v1.0"})
    
    
    response = client.post("/prompt", json={"question": "What is AI?"})
    assert response.status_code == 200
    assert "answer" in response.json()
    assert "sci_score" in response.json()

def test_stop_model():
    client.post("/deploy", json={"model_type": "text-generation", "model_name": "TinyLlama/TinyLlama-1.1B-Chat-v1.0"})
    response = client.post("/stop")
    assert response.status_code == 200
    assert response.json()["message"] == "Model stopped successfully"

def test_status():
    response = client.get("/status")
    assert response.status_code == 200
    assert response.json()["status"] == "No model deployed"
