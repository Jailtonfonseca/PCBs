from flask import Flask, render_template, request

from core.orchestrator import DesignOrchestrator
from core.requirements import PowerSupplyRequirements

# Initialize the Flask application
app = Flask(__name__)

# Instantiate the Design Orchestrator, which is now the main entry point
orchestrator = DesignOrchestrator()

@app.route('/')
def index():
    """
    Serves the main page with a simple text area for the user's request.
    """
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_schematic():
    """
    Handles the user's request, orchestrates the design, and displays the result.
    """
    user_request = request.form['user_request']

    # For this PoC, we still need to provide some hard-coded detailed requirements
    # until the AI can extract these from the user_request itself.
    # The AI's plan will determine which components are used.
    # These values are used for net naming and component selection logic.
    requirements = PowerSupplyRequirements(
        block_name="AI Generated Power Supply",
        input_voltage_v=12.0,
        output_voltage_v=5.0,
        max_output_current_a=1.0
    )

    # Use the orchestrator to create the schematic from the high-level request
    schematic, design_plan = orchestrator.create_schematic_from_request(
        user_request,
        requirements
    )

    # Render the result page, passing the schematic and the AI's plan
    return render_template('schematic.html', schematic=schematic, plan=design_plan, user_request=user_request)


if __name__ == '__main__':
    # Running in debug mode for development on port 5001
    app.run(debug=True, port=5001)