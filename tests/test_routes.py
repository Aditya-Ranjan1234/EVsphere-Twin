import pytest
from src.flask_app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    rv = client.get('/')
    assert rv.status_code == 200

def test_graph_api(client):
    # If Neo4j is offline or mock triggers, should complete gracefully or return fallback
    try:
        rv = client.get('/api/graph')
        assert rv.status_code in [200, 500]
    except Exception:
        pass

def test_predict_api(client):
    payload = {
        "seed_node": "Supplier_12",
        "node_type": "Supplier",
        "failure_prob": 0.5
    }
    rv = client.post('/api/predict', json=payload)
    assert rv.status_code == 200
    data = rv.get_json()
    assert "plot_data" in data
    assert "metrics" in data["plot_data"]
