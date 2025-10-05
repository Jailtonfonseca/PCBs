import pytest
from core.orchestrator import DesignOrchestrator
from core.requirements import PowerSupplyRequirements
from core.schematic import Schematic

@pytest.fixture
def orchestrator():
    """Provides a DesignOrchestrator instance for tests."""
    return DesignOrchestrator()

@pytest.fixture
def requirements():
    """Provides a standard set of PowerSupplyRequirements."""
    return PowerSupplyRequirements(
        block_name="Test 5V Supply",
        input_voltage_v=12.0,
        output_voltage_v=5.0,
        max_output_current_a=1.0
    )

def test_create_schematic_from_valid_request(orchestrator, requirements):
    """
    Tests the full orchestration process from a valid user request to a final schematic.
    """
    user_request = "I need a 5V power supply for my Arduino project."

    schematic, plan = orchestrator.create_schematic_from_request(user_request, requirements)

    # Check that a valid plan was generated and returned
    assert plan is not None
    assert len(plan) == 3
    assert plan == ["add_regulator_5v", "add_input_capacitor", "add_output_capacitor"]

    # Check that the final schematic is correctly assembled
    assert schematic is not None
    assert isinstance(schematic, Schematic)
    assert len(schematic.components) == 3
    assert len(schematic.nets) == 3

    # Spot-check for a component to ensure the generator was called
    u1 = next((c for c in schematic.components if c.reference_designator == "U1"), None)
    assert u1 is not None
    assert u1.part_number == "LM7805"

def test_create_schematic_from_unknown_request(orchestrator, requirements):
    """
    Tests that the orchestrator handles an unknown user request gracefully
    by returning an empty schematic and an empty plan.
    """
    user_request = "Please design a time machine."

    schematic, plan = orchestrator.create_schematic_from_request(user_request, requirements)

    # Check that the plan is empty
    assert plan is not None
    assert len(plan) == 0

    # Check that the schematic is empty
    assert schematic is not None
    assert isinstance(schematic, Schematic)
    assert len(schematic.components) == 0
    assert len(schematic.nets) == 0