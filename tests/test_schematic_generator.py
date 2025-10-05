import pytest
from core.requirements import PowerSupplyRequirements
from core.schematic_generator import SchematicGenerator
from core.schematic import Schematic, Component, Net

@pytest.fixture
def generator():
    """Provides a SchematicGenerator instance for tests."""
    return SchematicGenerator()

def test_generate_schematic_for_valid_5v_requirements(generator):
    """
    Tests that the generator successfully creates a schematic for valid 5V requirements.
    """
    requirements = PowerSupplyRequirements(
        block_name="Test 5V Supply",
        input_voltage_v=12.0,
        output_voltage_v=5.0,
        max_output_current_a=1.0
    )

    schematic = generator.generate(requirements)

    assert schematic is not None
    assert isinstance(schematic, Schematic)

    # Check for correct number of components and nets
    assert len(schematic.components) == 3
    assert len(schematic.nets) == 3

    # Check that the main components exist
    ref_des = [c.reference_designator for c in schematic.components]
    assert "U1" in ref_des
    assert "C1" in ref_des
    assert "C2" in ref_des

    # Check that the main nets exist
    net_names = [n.name for n in schematic.nets]
    assert "VIN_12.0V" in net_names
    assert "VOUT_5.0V" in net_names
    assert "GND" in net_names

    # Spot-check a connection
    vout_net = schematic.find_net("VOUT_5.0V")
    assert vout_net is not None

    u1 = next((c for c in schematic.components if c.reference_designator == "U1"), None)
    assert u1 is not None

    u1_out_pin = u1.get_pin("OUT")
    assert u1_out_pin in vout_net.pins

def test_generate_schematic_for_unsupported_voltage(generator):
    """
    Tests that the generator returns None for requirements it cannot fulfill (e.g., 3.3V).
    """
    requirements = PowerSupplyRequirements(
        block_name="Test 3.3V Supply",
        input_voltage_v=12.0,
        output_voltage_v=3.3,
        max_output_current_a=1.0
    )

    schematic = generator.generate(requirements)

    assert schematic is None

def test_generate_schematic_for_insufficient_input_voltage(generator):
    """
    Tests that the generator returns None when the input voltage is too low for the 5V rule.
    """
    requirements = PowerSupplyRequirements(
        block_name="Test Low Vin Supply",
        input_voltage_v=6.0, # LM7805 requires >= 7V
        output_voltage_v=5.0,
        max_output_current_a=1.0
    )

    schematic = generator.generate(requirements)

    assert schematic is None

def test_gnd_net_is_shared_correctly(generator):
    """
    Tests that all components that should connect to GND are on the same GND net.
    """
    requirements = PowerSupplyRequirements(
        block_name="Test 5V Supply",
        input_voltage_v=9.0,
        output_voltage_v=5.0,
        max_output_current_a=0.5
    )

    schematic = generator.generate(requirements)
    assert schematic is not None

    gnd_net = schematic.find_net("GND")
    assert gnd_net is not None

    # GND net should have 3 connections in the LM7805 circuit
    assert len(gnd_net.pins) == 3

    # Check that U1, C1, and C2 are all connected to the GND net
    connected_components = {pin.component_ref_des for pin in gnd_net.pins}
    assert "U1" in connected_components
    assert "C1" in connected_components
    assert "C2" in connected_components