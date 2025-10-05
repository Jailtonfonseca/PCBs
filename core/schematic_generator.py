"""
Service to generate a schematic based on provided requirements.
"""
from core.requirements import PowerSupplyRequirements
from core.schematic import Schematic, Component, Net, Pin

# A simple, hard-coded component library for the PoC.
# In a real system, this would be a sophisticated database service.
COMPONENT_LIBRARY = {
    "LM7805": {
        "description": "5V Positive Voltage Regulator",
        "pins": ["IN", "GND", "OUT"]
    },
    "CAP_10uF": {
        "description": "10uF Electrolytic Capacitor",
        "pins": ["1", "2"]
    },
    "CAP_0.1uF": {
        "description": "0.1uF Ceramic Capacitor",
        "pins": ["1", "2"]
    }
}

class SchematicGenerator:
    """
    Generates a schematic from a set of requirements.
    """
    def generate(self, requirements: PowerSupplyRequirements) -> (Schematic or None, str or None):
        """
        Generates a schematic for the given power supply requirements.

        Returns a tuple: (schematic, error_message).
        On success, error_message is None.
        On failure, schematic is None.
        """
        # Rule 0: Basic physical validation
        if requirements.input_voltage_v <= requirements.output_voltage_v:
            error = "Input voltage must be greater than output voltage."
            print(f"Validation Error: {error}")
            return None, error

        # Rule 1: LM7805 5V regulator
        if requirements.output_voltage_v == 5.0 and requirements.input_voltage_v >= 7.0:
            schematic = self._generate_lm7805_circuit(requirements)
            return schematic, None

        # Default case if no specific rule matches
        error = f"No generator rule found for the specified requirements: {requirements.output_voltage_v}V output."
        print(f"Warning: {error}")
        return None, error

    def _generate_lm7805_circuit(self, requirements: PowerSupplyRequirements) -> Schematic:
        """
        Generates a schematic for a standard LM7805-based 5V power supply.
        """
        schematic = Schematic()

        # 1. Create component instances
        u1 = Component(
            reference_designator="U1",
            part_number="LM7805",
            description=COMPONENT_LIBRARY["LM7805"]["description"]
        )
        c1 = Component(
            reference_designator="C1",
            part_number="CAP_10uF",
            description=f"Input Capacitor ({COMPONENT_LIBRARY['CAP_10uF']['description']})"
        )
        c2 = Component(
            reference_designator="C2",
            part_number="CAP_0.1uF",
            description=f"Output Capacitor ({COMPONENT_LIBRARY['CAP_0.1uF']['description']})"
        )

        schematic.add_component(u1)
        schematic.add_component(c1)
        schematic.add_component(c2)

        # 2. Create nets
        # We use get_or_create_net to avoid creating duplicate nets
        vin_net = schematic.get_or_create_net(f"VIN_{requirements.input_voltage_v}V")
        vout_net = schematic.get_or_create_net(f"VOUT_{requirements.output_voltage_v}V")
        gnd_net = schematic.get_or_create_net("GND")

        # 3. Connect component pins to nets
        # Input side
        vin_net.add_connection(u1.get_pin("IN"))
        vin_net.add_connection(c1.get_pin("1"))
        gnd_net.add_connection(c1.get_pin("2"))

        # Regulator
        gnd_net.add_connection(u1.get_pin("GND"))

        # Output side
        vout_net.add_connection(u1.get_pin("OUT"))
        vout_net.add_connection(c2.get_pin("1"))
        gnd_net.add_connection(c2.get_pin("2"))

        return schematic