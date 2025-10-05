"""
Functions to gather requirements data via command-line input and
create instances of the dataclasses defined in core.requirements.
"""
from typing import Optional, List

from core.requirements import ProjectRequirements, PowerSupplyRequirements

def prompt_for_project_requirements() -> ProjectRequirements:
    """
    Prompts the user for overall project requirements and returns a ProjectRequirements instance.

    Handles potential ValueError for numeric inputs, allowing optional fields to remain None
    if input is empty or invalid after a warning.
    """
    project_name = input("Enter project name: ").strip()
    if not project_name:
        print("Project name cannot be empty.")
        # For a real CLI, might loop until valid input or allow quitting
        return ProjectRequirements(project_name="Default Project")


    max_length_mm: Optional[float] = None
    try:
        length_str = input("Enter maximum PCB length in mm (optional, press Enter to skip): ").strip()
        if length_str:
            max_length_mm = float(length_str)
    except ValueError:
        print("Invalid input for length. Setting to None.")

    max_width_mm: Optional[float] = None
    try:
        width_str = input("Enter maximum PCB width in mm (optional, press Enter to skip): ").strip()
        if width_str:
            max_width_mm = float(width_str)
    except ValueError:
        print("Invalid input for width. Setting to None.")

    target_cost_usd: Optional[float] = None
    try:
        cost_str = input("Enter target manufacturing cost in USD (optional, press Enter to skip): ").strip()
        if cost_str:
            target_cost_usd = float(cost_str)
    except ValueError:
        print("Invalid input for cost. Setting to None.")

    return ProjectRequirements(
        project_name=project_name,
        max_length_mm=max_length_mm,
        max_width_mm=max_width_mm,
        target_cost_usd=target_cost_usd
    )

def prompt_for_power_supply_requirements() -> Optional[PowerSupplyRequirements]:
    """
    Prompts the user for specific power supply block requirements and
    returns a PowerSupplyRequirements instance.

    Handles potential ValueError for numeric inputs. If critical numeric inputs
    are invalid, this function might return None or raise an error after printing a message.
    """
    block_name = input("Enter power supply block name (e.g., 'Main 5V Rail'): ").strip()
    if not block_name:
        print("Power supply block name cannot be empty.")
        return None # Or re-prompt in a loop

    input_voltage_v: Optional[float] = None
    try:
        iv_str = input("Enter input voltage in Volts (e.g., 12.0): ").strip()
        input_voltage_v = float(iv_str)
    except ValueError:
        print("Invalid input for input voltage. This field is mandatory.")
        return None

    output_voltage_v: Optional[float] = None
    try:
        ov_str = input("Enter desired output voltage in Volts (e.g., 5.0): ").strip()
        output_voltage_v = float(ov_str)
    except ValueError:
        print("Invalid input for output voltage. This field is mandatory.")
        return None

    max_output_current_a: Optional[float] = None
    try:
        oc_str = input("Enter maximum output current in Amperes (e.g., 1.5): ").strip()
        max_output_current_a = float(oc_str)
    except ValueError:
        print("Invalid input for maximum output current. This field is mandatory.")
        return None

    protection_features_str = input(
        "Enter desired protection features, comma-separated (optional, e.g., short-circuit,over-voltage): "
    ).strip()
    
    protection_features: List[str] = []
    if protection_features_str:
        protection_features = [feature.strip() for feature in protection_features_str.split(',')]

    # Ensure mandatory fields were successfully converted
    if input_voltage_v is None or output_voltage_v is None or max_output_current_a is None:
        print("Failed to create power supply requirements due to missing mandatory numeric values.")
        return None

    return PowerSupplyRequirements(
        block_name=block_name,
        input_voltage_v=input_voltage_v,
        output_voltage_v=output_voltage_v,
        max_output_current_a=max_output_current_a,
        protection_features=protection_features
    )

from core.schematic import Schematic
from core.schematic_generator import SchematicGenerator


def display_schematic(schematic: Schematic):
    """Prints a human-readable summary of the schematic to the console."""
    if not schematic:
        print("No schematic to display.")
        return

    print("\n--- Generated Schematic ---")
    print("Components:")
    for comp in schematic.components:
        print(f"  - {comp.reference_designator}: {comp.part_number} ({comp.description})")

    print("\nNets:")
    for net in schematic.nets:
        connections = ", ".join([f"{pin.component_ref_des}.{pin.pin_name}" for pin in net.pins])
        print(f"  - {net.name}: connects [{connections}]")
    print("-------------------------\n")


if __name__ == '__main__':
    print("--- Project Requirements Input ---")
    project_reqs = prompt_for_project_requirements()
    print("\n--- Created Project Requirements ---")
    print(project_reqs)

    # Instantiate the generator
    generator = SchematicGenerator()

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
            print(f"\nAttempting to generate schematic for '{psu_req.block_name}'...")
            # Generate the schematic for the newly added power supply
            generated_schematic = generator.generate(psu_req)
            if generated_schematic:
                print("Schematic generated successfully!")
                display_schematic(generated_schematic)
            else:
                print("Could not generate a schematic for the specified requirements.")
        else:
            print("Skipping invalid power supply block.")

    if power_supplies:
        print("\n--- Summary: All Created Power Supply Requirements ---")
        for psu in power_supplies:
            print(psu)
    else:
        print("\nNo power supply blocks were added.")
