import pytest
from app import app as flask_app

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    flask_app.config.update({"TESTING": True})
    yield flask_app

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

def test_index_page_loads(client):
    """Test that the index page loads correctly with the new UI."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Describe the circuit you want to design" in response.data
    assert b"Your Request:" in response.data

def test_generate_design_with_valid_request(client):
    """
    Test the /generate endpoint with a valid user request that the AI can handle.
    """
    response = client.post('/generate', data={
        'user_request': 'I need a 5V power supply.'
    })
    assert response.status_code == 200
    # Check for the new sections in the results page
    assert b"Design Result" in response.data
    assert b"Your Request" in response.data
    assert b"AI-Generated Plan" in response.data
    assert b"Final Schematic" in response.data

    # Check for plan and schematic content
    assert b"add_regulator_5v" in response.data
    assert b"U1" in response.data
    assert b"LM7805" in response.data

def test_generate_design_with_unknown_request(client):
    """
    Test the /generate endpoint with a user request that the AI cannot handle.
    """
    response = client.post('/generate', data={
        'user_request': 'Build me a spaceship.'
    })
    assert response.status_code == 200
    assert b"Design Failed" in response.data
    assert b"The AI could not generate a design plan" in response.data
    # Ensure no schematic content is displayed
    assert b"Final Schematic" not in response.data