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
    Executes single-step commands to build a schematic incrementally.
    """
    def execute_command(self, command: str, schematic: Schematic, requirements: PowerSupplyRequirements):
        """
        Executes a single design command and modifies the schematic in place.

        Args:
            command: The command to execute (e.g., 'add_regulator_5v').
            schematic: The schematic object to modify.
            requirements: The overall project requirements.
        """
        if command == "add_regulator_5v":
            self._add_lm7805_regulator(schematic, requirements)
        elif command == "add_input_capacitor":
            self._add_input_capacitor(schematic, requirements)
        elif command == "add_output_capacitor":
            self._add_output_capacitor(schematic, requirements)
        else:
            print(f"Warning: Unknown command '{command}' ignored.")

    def _add_lm7805_regulator(self, schematic: Schematic, requirements: PowerSupplyRequirements):
        """Adds and connects an LM7805 regulator."""
        u1 = Component(
            reference_designator="U1",
            part_number="LM7805",
            description=COMPONENT_LIBRARY["LM7805"]["description"]
        )
        schematic.add_component(u1)

        vin_net = schematic.get_or_create_net(f"VIN_{requirements.input_voltage_v}V")
        vout_net = schematic.get_or_create_net(f"VOUT_{requirements.output_voltage_v}V")
        gnd_net = schematic.get_or_create_net("GND")

        vin_net.add_connection(u1.get_pin("IN"))
        vout_net.add_connection(u1.get_pin("OUT"))
        gnd_net.add_connection(u1.get_pin("GND"))
        print("Executed: add_regulator_5v")

    def _add_input_capacitor(self, schematic: Schematic, requirements: PowerSupplyRequirements):
        """Adds and connects the input capacitor."""
        c1 = Component(
            reference_designator="C1",
            part_number="CAP_10uF",
            description=f"Input Capacitor ({COMPONENT_LIBRARY['CAP_10uF']['description']})"
        )
        schematic.add_component(c1)

        vin_net = schematic.get_or_create_net(f"VIN_{requirements.input_voltage_v}V")
        gnd_net = schematic.get_or_create_net("GND")

        vin_net.add_connection(c1.get_pin("1"))
        gnd_net.add_connection(c1.get_pin("2"))
        print("Executed: add_input_capacitor")

    def _add_output_capacitor(self, schematic: Schematic, requirements: PowerSupplyRequirements):
        """Adds and connects the output capacitor."""
        c2 = Component(
            reference_designator="C2",
            part_number="CAP_0.1uF",
            description=f"Output Capacitor ({COMPONENT_LIBRARY['CAP_0.1uF']['description']})"
        )
        schematic.add_component(c2)

        vout_net = schematic.get_or_create_net(f"VOUT_{requirements.output_voltage_v}V")
        gnd_net = schematic.get_or_create_net("GND")

        vout_net.add_connection(c2.get_pin("1"))
        gnd_net.add_connection(c2.get_pin("2"))
        print("Executed: add_output_capacitor")