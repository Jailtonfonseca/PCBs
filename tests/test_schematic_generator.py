import pytest
from core.requirements import PowerSupplyRequirements
from core.schematic_generator import SchematicGenerator
from core.schematic import Schematic

@pytest.fixture
def generator():
    """Provides a SchematicGenerator instance for tests."""
    return SchematicGenerator()

@pytest.fixture
def empty_schematic():
    """Provides a fresh, empty Schematic instance for each test."""
    return Schematic()

@pytest.fixture
def requirements():
    """Provides a standard set of PowerSupplyRequirements."""
    return PowerSupplyRequirements(
        block_name="Test 5V Supply",
        input_voltage_v=12.0,
        output_voltage_v=5.0,
        max_output_current_a=1.0
    )

def test_add_lm7805_regulator(generator, empty_schematic, requirements):
    """Tests that the 'add_regulator_5v' command adds a regulator and connects its pins."""
    schematic = empty_schematic
    generator.execute_command("add_regulator_5v", schematic, requirements)

    assert len(schematic.components) == 1
    u1 = schematic.components[0]
    assert u1.part_number == "LM7805"

    vin_net = schematic.find_net("VIN_12.0V")
    vout_net = schematic.find_net("VOUT_5.0V")
    gnd_net = schematic.find_net("GND")

    assert vin_net is not None
    assert vout_net is not None
    assert gnd_net is not None

    assert u1.get_pin("IN") in vin_net.pins
    assert u1.get_pin("OUT") in vout_net.pins
    assert u1.get_pin("GND") in gnd_net.pins

def test_add_input_capacitor(generator, empty_schematic, requirements):
    """Tests that the 'add_input_capacitor' command adds a capacitor to the input net."""
    schematic = empty_schematic
    generator.execute_command("add_input_capacitor", schematic, requirements)

    assert len(schematic.components) == 1
    c1 = schematic.components[0]
    assert c1.part_number == "CAP_10uF"

    vin_net = schematic.find_net("VIN_12.0V")
    gnd_net = schematic.find_net("GND")

    assert vin_net is not None
    assert gnd_net is not None

    assert c1.get_pin("1") in vin_net.pins
    assert c1.get_pin("2") in gnd_net.pins

def test_add_output_capacitor(generator, empty_schematic, requirements):
    """Tests that the 'add_output_capacitor' command adds a capacitor to the output net."""
    schematic = empty_schematic
    generator.execute_command("add_output_capacitor", schematic, requirements)

    assert len(schematic.components) == 1
    c2 = schematic.components[0]
    assert c2.part_number == "CAP_0.1uF"

    vout_net = schematic.find_net("VOUT_5.0V")
    gnd_net = schematic.find_net("GND")

    assert vout_net is not None
    assert gnd_net is not None

    assert c2.get_pin("1") in vout_net.pins
    assert c2.get_pin("2") in gnd_net.pins

def test_unknown_command_is_ignored(generator, empty_schematic, requirements):
    """Tests that an unknown command does not add any components."""
    schematic = empty_schematic
    generator.execute_command("make_coffee", schematic, requirements)
    assert len(schematic.components) == 0