"""
Functions to gather requirements data via command-line input and
create instances of the dataclasses defined in core.requirements.
"""
from typing import Optional, List

from core.requirements import ProjectRequirements, PowerSupplyRequirements

def _prompt_for_float_input(prompt_message: str, is_mandatory: bool = False) -> Optional[float]:
    """
    Helper function to prompt the user for a float input.

    Args:
        prompt_message (str): The message to display to the user.
        is_mandatory (bool): If True, the loop continues until a valid float is entered.
                             If False, an empty input is accepted as None.

    Returns:
        Optional[float]: The float value entered by the user, or None if input is empty
                         and not mandatory.
    """
    while True:
        user_input = input(prompt_message).strip()
        if not user_input:  # Empty input
            if is_mandatory:
                print("This field is mandatory. Please enter a value.")
                continue
            else:
                return None
        try:
            return float(user_input)
        except ValueError:
            print("Invalid input. Please enter a valid number (e.g., 10.5) or leave blank if optional.")
            # Loop continues for both mandatory and optional if input is provided but invalid

def prompt_for_project_requirements() -> ProjectRequirements:
    """
    Prompts the user for overall project requirements and returns a ProjectRequirements instance.
    """
    while True:
        project_name = input("Enter project name: ").strip()
        if project_name:
            break
        print("Project name cannot be empty. Please try again.")

    max_length_mm = _prompt_for_float_input(
        "Enter maximum PCB length in mm (optional, press Enter to skip): ",
        is_mandatory=False
    )
    max_width_mm = _prompt_for_float_input(
        "Enter maximum PCB width in mm (optional, press Enter to skip): ",
        is_mandatory=False
    )
    target_cost_usd = _prompt_for_float_input(
        "Enter target manufacturing cost in USD (optional, press Enter to skip): ",
        is_mandatory=False
    )

    return ProjectRequirements(
        project_name=project_name,
        max_length_mm=max_length_mm,
        max_width_mm=max_width_mm,
        target_cost_usd=target_cost_usd
    )

def prompt_for_power_supply_requirements() -> Optional[PowerSupplyRequirements]:
    """
    Prompts the user for specific power supply block requirements and
    returns a PowerSupplyRequirements instance, or None if critical info is missing.
    """
    while True:
        block_name = input("Enter power supply block name (e.g., 'Main 5V Rail'): ").strip()
        if block_name:
            break
        print("Power supply block name cannot be empty. Please try again.")

    # These calls will loop until valid float input is received because is_mandatory=True
    input_voltage_v = _prompt_for_float_input(
        "Enter input voltage in Volts (e.g., 12.0): ",
        is_mandatory=True
    )
    output_voltage_v = _prompt_for_float_input(
        "Enter desired output voltage in Volts (e.g., 5.0): ",
        is_mandatory=True
    )
    max_output_current_a = _prompt_for_float_input(
        "Enter maximum output current in Amperes (e.g., 1.5): ",
        is_mandatory=True
    )

    protection_features_str = input(
        "Enter desired protection features, comma-separated (optional, e.g., short-circuit,over-voltage): "
    ).strip()
    
    protection_features: List[str] = []
    if protection_features_str:
        protection_features = [feature.strip() for feature in protection_features_str.split(',')]

    # The helper function _prompt_for_float_input with is_mandatory=True ensures these are floats.
    # So, direct assignment is safe here. The function won't proceed past those prompts
    # unless valid floats are entered.
    return PowerSupplyRequirements(
        block_name=block_name,
        input_voltage_v=input_voltage_v, # type: ignore
        output_voltage_v=output_voltage_v, # type: ignore
        max_output_current_a=max_output_current_a, # type: ignore
        protection_features=protection_features
    )

if __name__ == '__main__':
    print("--- Project Requirements Input ---")
    project_reqs = prompt_for_project_requirements()
    print("\n--- Created Project Requirements ---")
    print(project_reqs)

    print("\n--- Power Supply Requirements Input ---")
    # Example of adding multiple power supplies
    power_supplies: List[PowerSupplyRequirements] = []
    while True:
        add_another = input("Add a power supply block? (yes/no, default no): ").strip().lower()
        if add_another != 'yes':
            break
        psu_req = prompt_for_power_supply_requirements()
        if psu_req:
            power_supplies.append(psu_req)
        else:
            print("Skipping invalid power supply block.")

    if power_supplies:
        print("\n--- Created Power Supply Requirements ---")
        for psu in power_supplies:
            print(psu)
    else:
        print("\nNo power supply blocks were added.")
