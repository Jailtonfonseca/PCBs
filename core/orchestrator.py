"""
The DesignOrchestrator coordinates the AI strategy and schematic generation services.
"""
from typing import List, Tuple

from core.ai_strategy import AIStrategyService
from core.requirements import PowerSupplyRequirements
from core.schematic import Schematic
from core.schematic_generator import SchematicGenerator

class DesignOrchestrator:
    """
    Coordinates the entire design process, from user request to final schematic.
    """
    def __init__(self):
        self.ai_strategy_service = AIStrategyService()
        self.schematic_generator = SchematicGenerator()

    def create_schematic_from_request(
        self,
        user_request: str,
        requirements: PowerSupplyRequirements
    ) -> Tuple[Schematic, List[str]]:
        """
        Orchestrates the design process.

        1. Gets a design plan from the AI Strategy Service.
        2. Executes the plan step-by-step using the Schematic Generator.
        3. Returns the final schematic and the plan that was executed.

        Args:
            user_request: The user's natural language request.
            requirements: The detailed, parameterized requirements.

        Returns:
            A tuple containing the generated schematic and the design plan.
        """
        print("Orchestrator: Starting design process.")

        # 1. Get the design plan from the AI
        design_plan = self.ai_strategy_service.get_design_plan(user_request)

        # 2. Create an empty schematic to build upon
        schematic = Schematic()

        # 3. Execute the plan step-by-step
        if not design_plan:
            print("Orchestrator: AI returned an empty plan. Nothing to generate.")
        else:
            print(f"Orchestrator: Executing AI plan: {design_plan}")
            for command in design_plan:
                self.schematic_generator.execute_command(command, schematic, requirements)

        print("Orchestrator: Design process complete.")
        return schematic, design_plan

if __name__ == '__main__':
    # Example Usage
    orchestrator = DesignOrchestrator()

    # Define a user request and the corresponding detailed requirements
    request = "Please design a 5V power supply for me."
    reqs = PowerSupplyRequirements(
        block_name="5V PSU",
        input_voltage_v=12.0,
        output_voltage_v=5.0,
        max_output_current_a=1.0
    )

    # Run the orchestration
    final_schematic, plan = orchestrator.create_schematic_from_request(request, reqs)

    # Verify the output
    print("\n--- Orchestration Complete ---")
    print(f"Executed Plan: {plan}")
    print("\nFinal Schematic Components:")
    for comp in final_schematic.components:
        print(f"  - {comp.reference_designator}: {comp.part_number}")

    print("\nFinal Schematic Nets:")
    for net in final_schematic.nets:
        connections = ", ".join([f"{pin.component_ref_des}.{pin.pin_name}" for pin in net.pins])
        print(f"  - {net.name}: connects [{connections}]")

    assert len(final_schematic.components) == 3
    assert len(final_schematic.nets) == 3
    assert plan is not None