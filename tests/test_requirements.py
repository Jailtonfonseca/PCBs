"""
Unit tests for core.requirements and core.requirements_parser.
"""
import unittest
from unittest.mock import patch

from core.requirements import ProjectRequirements, PowerSupplyRequirements
from core.requirements_parser import prompt_for_project_requirements, prompt_for_power_supply_requirements

class TestRequirementsDataStructures(unittest.TestCase):
    """Tests for the data structure classes in core.requirements."""

    def test_project_requirements_creation(self):
        """Test creation of ProjectRequirements instances."""
        # Test with all fields
        req1 = ProjectRequirements(
            project_name="Test Project 1",
            max_length_mm=100.0,
            max_width_mm=50.0,
            target_cost_usd=20.0
        )
        self.assertEqual(req1.project_name, "Test Project 1")
        self.assertEqual(req1.max_length_mm, 100.0)
        self.assertEqual(req1.max_width_mm, 50.0)
        self.assertEqual(req1.target_cost_usd, 20.0)

        # Test with optional fields missing
        req2 = ProjectRequirements(project_name="Test Project 2")
        self.assertEqual(req2.project_name, "Test Project 2")
        self.assertIsNone(req2.max_length_mm)
        self.assertIsNone(req2.max_width_mm)
        self.assertIsNone(req2.target_cost_usd)

        # Test with some optional fields
        req3 = ProjectRequirements(project_name="Test Project 3", max_length_mm=120.5)
        self.assertEqual(req3.project_name, "Test Project 3")
        self.assertEqual(req3.max_length_mm, 120.5)
        self.assertIsNone(req3.max_width_mm)
        self.assertIsNone(req3.target_cost_usd)

    def test_power_supply_requirements_creation(self):
        """Test creation of PowerSupplyRequirements instances."""
        # Test with all fields including protection features
        psu1 = PowerSupplyRequirements(
            block_name="Main 5V",
            input_voltage_v=12.0,
            output_voltage_v=5.0,
            max_output_current_a=1.0,
            protection_features=["short-circuit", "over-voltage"]
        )
        self.assertEqual(psu1.block_name, "Main 5V")
        self.assertEqual(psu1.input_voltage_v, 12.0)
        self.assertEqual(psu1.output_voltage_v, 5.0)
        self.assertEqual(psu1.max_output_current_a, 1.0)
        self.assertEqual(psu1.protection_features, ["short-circuit", "over-voltage"])

        # Test with empty protection features (default)
        psu2 = PowerSupplyRequirements(
            block_name="Analog 3.3V",
            input_voltage_v=5.0,
            output_voltage_v=3.3,
            max_output_current_a=0.5
        )
        self.assertEqual(psu2.block_name, "Analog 3.3V")
        self.assertEqual(psu2.input_voltage_v, 5.0)
        self.assertEqual(psu2.output_voltage_v, 3.3)
        self.assertEqual(psu2.max_output_current_a, 0.5)
        self.assertEqual(psu2.protection_features, []) # default_factory=list

        # Test with explicitly empty protection features list
        psu3 = PowerSupplyRequirements(
            block_name="Sensor 1.8V",
            input_voltage_v=3.3,
            output_voltage_v=1.8,
            max_output_current_a=0.2,
            protection_features=[]
        )
        self.assertEqual(psu3.protection_features, [])


class TestRequirementsParser(unittest.TestCase):
    """Tests for the input parsing functions in core.requirements_parser."""

    @patch('builtins.input')
    def test_prompt_for_project_requirements_valid_input(self, mock_input):
        """Test parsing valid full input for project requirements."""
        mock_input.side_effect = [
            "My Awesome Project",  # project_name
            "120.5",               # max_length_mm
            "75.2",                # max_width_mm
            "30.0"                 # target_cost_usd
        ]
        req = prompt_for_project_requirements()
        self.assertEqual(req.project_name, "My Awesome Project")
        self.assertEqual(req.max_length_mm, 120.5)
        self.assertEqual(req.max_width_mm, 75.2)
        self.assertEqual(req.target_cost_usd, 30.0)

    @patch('builtins.input')
    def test_prompt_for_project_requirements_empty_optionals(self, mock_input):
        """Test parsing with empty optional inputs for project requirements."""
        mock_input.side_effect = [
            "My Minimal Project",  # project_name
            "",                    # max_length_mm (empty)
            "",                    # max_width_mm (empty)
            ""                     # target_cost_usd (empty)
        ]
        req = prompt_for_project_requirements()
        self.assertEqual(req.project_name, "My Minimal Project")
        self.assertIsNone(req.max_length_mm)
        self.assertIsNone(req.max_width_mm)
        self.assertIsNone(req.target_cost_usd)

    @patch('builtins.input')
    def test_prompt_for_project_requirements_invalid_numeric(self, mock_input):
        """Test parsing with invalid numeric input for an optional field."""
        mock_input.side_effect = [
            "Project Invalid Numeric", # project_name
            "abc",                     # max_length_mm (invalid)
            "75",                      # max_width_mm
            ""                         # target_cost_usd (empty)
        ]
        # _prompt_for_float_input will re-prompt on "abc".
        # If the next input for that prompt is empty, it returns None.
        # So, the sequence is: "abc" (invalid) -> "" (valid for optional, results in None)
        req = prompt_for_project_requirements()
        self.assertEqual(req.project_name, "Project Invalid Numeric")
        self.assertIsNone(req.max_length_mm)
        self.assertEqual(req.max_width_mm, 75.0)
        self.assertIsNone(req.target_cost_usd)

    @patch('builtins.input')
    def test_prompt_for_power_supply_requirements_valid_input(self, mock_input):
        """Test parsing valid full input for power supply requirements."""
        mock_input.side_effect = [
            "Digital Core Supply",       # block_name
            "5.0",                       # input_voltage_v
            "3.3",                       # output_voltage_v
            "1.2",                       # max_output_current_a
            "short-circuit,over-voltage" # protection_features
        ]
        psu = prompt_for_power_supply_requirements()
        self.assertIsNotNone(psu)
        self.assertEqual(psu.block_name, "Digital Core Supply")
        self.assertEqual(psu.input_voltage_v, 5.0)
        self.assertEqual(psu.output_voltage_v, 3.3)
        self.assertEqual(psu.max_output_current_a, 1.2)
        self.assertEqual(psu.protection_features, ["short-circuit", "over-voltage"])

    @patch('builtins.input')
    def test_prompt_for_power_supply_requirements_empty_protection(self, mock_input):
        """Test parsing power supply requirements with empty protection features string."""
        mock_input.side_effect = [
            "Analog Front End", # block_name
            "12.0",             # input_voltage_v
            "5.0",              # output_voltage_v
            "0.5",              # max_output_current_a
            ""                  # protection_features (empty)
        ]
        psu = prompt_for_power_supply_requirements()
        self.assertIsNotNone(psu)
        self.assertEqual(psu.block_name, "Analog Front End")
        self.assertEqual(psu.input_voltage_v, 12.0)
        self.assertEqual(psu.output_voltage_v, 5.0)
        self.assertEqual(psu.max_output_current_a, 0.5)
        self.assertEqual(psu.protection_features, [])

    @patch('builtins.input')
    def test_prompt_for_power_supply_requirements_invalid_mandatory_numeric(self, mock_input):
        """Test parsing with invalid input for a mandatory numeric field."""
        mock_input.side_effect = [
            "Faulty Supply", # block_name
            "abc",           # input_voltage_v (invalid)
            "12.0",          # input_voltage_v (valid after re-prompt)
            "5.0",           # output_voltage_v
            "1.0",           # max_output_current_a
            ""               # protection_features
        ]
        psu = prompt_for_power_supply_requirements()
        self.assertIsNotNone(psu) # Function should now succeed
        self.assertEqual(psu.block_name, "Faulty Supply")
        self.assertEqual(psu.input_voltage_v, 12.0) # Should be the valid re-prompted value
        self.assertEqual(psu.output_voltage_v, 5.0)
        self.assertEqual(psu.max_output_current_a, 1.0)

    @patch('builtins.input')
    def test_prompt_for_project_requirements_empty_name(self, mock_input):
        """Test re-prompting for an empty project name."""
        mock_input.side_effect = [
            "",                     # project_name (empty, first attempt)
            "Valid Project Name",   # project_name (valid, second attempt)
            "100",                  # max_length_mm
            "100",                  # max_width_mm
            "10"                    # target_cost_usd
        ]
        req = prompt_for_project_requirements()
        self.assertEqual(req.project_name, "Valid Project Name")
        # Check if input was called at least twice for the name (initial prompt + re-prompt)
        # This is a bit fragile, depends on the exact number of input() calls for other fields.
        # A more robust way would be to check call_args_list for specific prompts if needed.
        self.assertGreaterEqual(mock_input.call_count, 5) # name, name, len, width, cost

    @patch('builtins.input')
    def test_prompt_for_power_supply_requirements_empty_block_name(self, mock_input):
        """Test re-prompting for an empty block name for power supply."""
        mock_input.side_effect = [
            "",                  # block_name (empty, first attempt)
            "Valid Block Name",  # block_name (valid, second attempt)
            "12.0",              # input_voltage_v
            "5.0",               # output_voltage_v
            "1.0",               # max_output_current_a
            ""                   # protection_features
        ]
        psu = prompt_for_power_supply_requirements()
        self.assertIsNotNone(psu)
        self.assertEqual(psu.block_name, "Valid Block Name")
        self.assertEqual(psu.input_voltage_v, 12.0)

if __name__ == '__main__':
    unittest.main()
