from flask import Flask, render_template, request, redirect, url_for

from core.requirements import PowerSupplyRequirements
from core.schematic_generator import SchematicGenerator

# Initialize the Flask application
app = Flask(__name__)

# Instantiate the schematic generator
generator = SchematicGenerator()

@app.route('/')
def index():
    """
    Serves the main page with the input form.
    """
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_schematic():
    """
    Handles the form submission, generates the schematic, and displays the result.
    """
    try:
        # Extract form data
        block_name = request.form['block_name']
        input_voltage = float(request.form['input_voltage'])
        output_voltage = float(request.form['output_voltage'])
        max_current = float(request.form['max_current'])

        # Create requirements object
        requirements = PowerSupplyRequirements(
            block_name=block_name,
            input_voltage_v=input_voltage,
            output_voltage_v=output_voltage,
            max_output_current_a=max_current
        )

        # Generate the schematic
        schematic = generator.generate(requirements)

        # Render the result page
        return render_template('schematic.html', schematic=schematic)

    except (ValueError, KeyError) as e:
        # Handle cases where form data is missing or not a valid number
        return f"Error: Invalid form data provided. {e}", 400


if __name__ == '__main__':
    # Running in debug mode for development on port 5001
    app.run(debug=True, port=5001)