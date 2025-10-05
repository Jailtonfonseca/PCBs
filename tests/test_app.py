import pytest
from app import app as flask_app

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # The app is already created in app.py, we just need to configure it for testing
    flask_app.config.update({
        "TESTING": True,
    })
    yield flask_app

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

def test_index_page_loads(client):
    """Test that the index page loads correctly."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Define your power supply requirements" in response.data

def test_generate_schematic_with_valid_data(client):
    """
    Test the /generate endpoint with valid form data that should result
    in a successful schematic generation.
    """
    response = client.post('/generate', data={
        'block_name': 'Test 5V Supply',
        'input_voltage': '12.0',
        'output_voltage': '5.0',
        'max_current': '1.0'
    })
    assert response.status_code == 200
    assert b"Generated Schematic" in response.data
    # Check for component and net names in the response
    assert b"U1" in response.data
    assert b"LM7805" in response.data
    assert b"VOUT_5.0V" in response.data
    assert b"GND" in response.data

def test_generate_schematic_with_unsupported_data(client):
    """
    Test the /generate endpoint with valid form data but for requirements
    that the generator cannot handle (e.g., 3.3V).
    """
    response = client.post('/generate', data={
        'block_name': 'Test 3.3V Supply',
        'input_voltage': '12.0',
        'output_voltage': '3.3',
        'max_current': '1.0'
    })
    assert response.status_code == 200
    assert b"Generation Failed" in response.data
    # Check for the specific error reason now displayed in the template
    assert b"Reason:" in response.data
    assert b"No generator rule found" in response.data

def test_generate_schematic_with_invalid_data(client):
    """
    Test the /generate endpoint with invalid or missing form data.
    The app should now render the error page gracefully with a 200 status.
    """
    # Missing 'max_current'
    response = client.post('/generate', data={
        'block_name': 'Test 5V Supply',
        'input_voltage': '12.0',
        'output_voltage': '5.0'
    })
    assert response.status_code == 200
    assert b"Generation Failed" in response.data
    assert b"Invalid or missing form data" in response.data