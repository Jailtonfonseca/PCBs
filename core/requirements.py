"""
Defines classes for representing parameterized requirements for electronics projects.
"""
from dataclasses import dataclass, field
from typing import Optional, List

@dataclass
class ProjectRequirements:
    """
    Represents the overall requirements for an electronics project.

    Attributes:
        project_name (str): Name of the project.
        max_length_mm (Optional[float]): Maximum length of the PCB in millimeters.
        max_width_mm (Optional[float]): Maximum width of the PCB in millimeters.
        target_cost_usd (Optional[float]): Target manufacturing cost in USD.
    """
    project_name: str
    max_length_mm: Optional[float] = None
    max_width_mm: Optional[float] = None
    target_cost_usd: Optional[float] = None

@dataclass
class PowerSupplyRequirements:
    """
    Represents the requirements for a specific power supply block within a project.

    Attributes:
        block_name (str): Descriptive name for this power supply block (e.g., "Main 5V Rail", "Analog Section Supply").
        input_voltage_v (float): Input voltage to the power supply in Volts.
        output_voltage_v (float): Desired output voltage from the power supply in Volts.
        max_output_current_a (float): Maximum output current the power supply must provide in Amperes.
        protection_features (List[str]): List of desired protection features (defaults to an empty list).
            Examples: ["short-circuit", "over-voltage", "thermal-shutdown", "reverse-polarity"].
    """
    block_name: str
    input_voltage_v: float
    output_voltage_v: float
    max_output_current_a: float
    protection_features: List[str] = field(default_factory=list)

if __name__ == '__main__':
    # Example Usage
    project_req = ProjectRequirements(
        project_name="IoT Weather Station",
        max_length_mm=100.0,
        max_width_mm=80.0,
        target_cost_usd=25.0
    )

    psu_req_5v = PowerSupplyRequirements(
        block_name="Main Digital Supply (5V)",
        input_voltage_v=12.0,
        output_voltage_v=5.0,
        max_output_current_a=1.5,
        protection_features=["short-circuit", "over-voltage"]
    )

    psu_req_3v3 = PowerSupplyRequirements(
        block_name="Analog Sensor Supply (3.3V)",
        input_voltage_v=5.0,  # Assuming this is fed from the main 5V supply
        output_voltage_v=3.3,
        max_output_current_a=0.5,
        protection_features=["short-circuit"]
    )

    print(project_req)
    print(psu_req_5v)
    print(psu_req_3v3)
