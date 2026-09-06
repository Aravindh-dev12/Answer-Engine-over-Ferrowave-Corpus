import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.indexer import CorpusIndex
from app.config import CORPUS_DIR

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["ok"] is True
    assert data["documents_indexed"] > 0
    assert "model" in data

def test_ask_empty_question(client):
    response = client.post("/ask", json={"question": "   "})
    assert response.status_code == 400

def test_ask_factual_export(client):
    response = client.post("/ask", json={"question": "How long are export files available for download?"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ["answered", "insufficient_evidence"]
    assert "diagnostics" in data
    assert data["diagnostics"]["latency_ms"] >= 0
    if data["citations"]:
        for cit in data["citations"]:
            assert len(cit["quote"]) <= 300
            # Ensure path does not leak internal docs
            assert "internal/" not in cit["path"]
            assert "draft" not in cit["path"].lower()

def test_ask_needs_clarification(client):
    response = client.post("/ask", json={"question": "What is my support response time?"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ["needs_clarification", "answered"]

def test_ask_insufficient_evidence(client):
    response = client.post("/ask", json={"question": "Does Ferrowave Pulse have an integration with quantum computing hardware?"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "insufficient_evidence"

def test_internal_docs_not_cited(client):
    # Testing that internal docs like RFC 0042 or SLA v4 draft are never exposed
    response = client.post("/ask", json={"question": "Tell me about RFC 0042 Salesforce v2 internal architecture"})
    assert response.status_code == 200
    data = response.json()
    for cit in data["citations"]:
        assert not cit["path"].startswith("internal/")
        assert "rfc-0042" not in cit["path"]
        assert "draft" not in cit["path"].lower()
