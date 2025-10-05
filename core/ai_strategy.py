"""
Simulates an AI service that creates a design plan from a user request.
In a real application, this would involve a call to a large language model (LLM).
"""
from typing import List

class AIStrategyService:
    """
    A mock service that returns a hard-coded design plan based on keywords
    in the user's request.
    """
    def get_design_plan(self, user_request: str) -> List[str]:
        """
        Parses the user request and returns a step-by-step design plan.

        Args:
            user_request: The natural language request from the user.

        Returns:
            A list of commands for the schematic generator.
        """
        request_lower = user_request.lower()

        # This is a very simple keyword-based mock. A real implementation
        # would use an LLM to generate a much more nuanced plan.
        if "5v" in request_lower and "power supply" in request_lower:
            print("AI Strategy: Detected request for a 5V power supply. Generating standard plan.")
            return [
                "add_regulator_5v",
                "add_input_capacitor",
                "add_output_capacitor"
            ]

        print(f"AI Strategy: No specific plan found for request: '{user_request}'. Returning empty plan.")
        return []

if __name__ == '__main__':
    # Example usage
    ai_service = AIStrategyService()

    # Test case 1: A request that should match a plan
    request1 = "I need a 5V power supply for my Arduino project."
    plan1 = ai_service.get_design_plan(request1)
    print(f"Request: '{request1}'")
    print(f"Generated Plan: {plan1}")
    assert plan1 == ["add_regulator_5v", "add_input_capacitor", "add_output_capacitor"]

    # Test case 2: A request that should not match a plan
    request2 = "Design a high-speed differential pair."
    plan2 = ai_service.get_design_plan(request2)
    print(f"\nRequest: '{request2}'")
    print(f"Generated Plan: {plan2}")
    assert plan2 == []