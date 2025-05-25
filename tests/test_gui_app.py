"""
Unit tests for the gui.app.RequirementsApp class.
"""
import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
from tkinter import ttk # Required for some app elements, even if not directly tested

from gui.app import RequirementsApp
from core.requirements import ProjectRequirements, PowerSupplyRequirements

class TestRequirementsApp(unittest.TestCase):
    """Tests for the RequirementsApp methods."""

    def setUp(self):
        """Set up the test environment for each test."""
        self.root_tk = tk.Tk()
        # Prevent the window from actually appearing during tests
        self.root_tk.withdraw()
        self.app = RequirementsApp(self.root_tk)

    def tearDown(self):
        """Clean up the test environment after each test."""
        # Check if root_tk exists and is not destroyed, then destroy
        if self.root_tk and self.root_tk.winfo_exists():
            self.root_tk.destroy()

    @patch('gui.app.messagebox')
    def test_save_project_requirements_valid_input(self, mock_messagebox):
        """Test _save_project_requirements with valid inputs."""
        self.app.entry_project_name.get = MagicMock(return_value="Test Project")
        self.app.entry_max_length.get = MagicMock(return_value="100.5")
        self.app.entry_max_width.get = MagicMock(return_value="50.2")
        self.app.entry_target_cost.get = MagicMock(return_value="25.0")

        self.app._save_project_requirements()

        self.assertIsNotNone(self.app.project_requirements)
        self.assertIsInstance(self.app.project_requirements, ProjectRequirements)
        self.assertEqual(self.app.project_requirements.project_name, "Test Project")
        self.assertEqual(self.app.project_requirements.max_length_mm, 100.5)
        self.assertEqual(self.app.project_requirements.max_width_mm, 50.2)
        self.assertEqual(self.app.project_requirements.target_cost_usd, 25.0)
        mock_messagebox.showinfo.assert_called_once_with("Success", "Project Requirements saved.")

    @patch('gui.app.messagebox')
    def test_save_project_requirements_valid_input_optional_empty(self, mock_messagebox):
        """Test _save_project_requirements with valid inputs and empty optionals."""
        self.app.entry_project_name.get = MagicMock(return_value="Test Optional Empty")
        self.app.entry_max_length.get = MagicMock(return_value="") # Empty optional
        self.app.entry_max_width.get = MagicMock(return_value=" ") # Empty optional with space
        self.app.entry_target_cost.get = MagicMock(return_value="") # Empty optional

        self.app._save_project_requirements()

        self.assertIsNotNone(self.app.project_requirements)
        self.assertEqual(self.app.project_requirements.project_name, "Test Optional Empty")
        self.assertIsNone(self.app.project_requirements.max_length_mm)
        self.assertIsNone(self.app.project_requirements.max_width_mm)
        self.assertIsNone(self.app.project_requirements.target_cost_usd)
        mock_messagebox.showinfo.assert_called_once_with("Success", "Project Requirements saved.")


    @patch('gui.app.messagebox')
    def test_save_project_requirements_empty_name(self, mock_messagebox):
        """Test _save_project_requirements with an empty project name."""
        self.app.entry_project_name.get = MagicMock(return_value="")
        self.app.entry_max_length.get = MagicMock(return_value="100") # Other fields don't matter here

        self.app._save_project_requirements()

        self.assertIsNone(self.app.project_requirements)
        mock_messagebox.showerror.assert_called_once_with("Validation Error", "Project Name cannot be empty.")

    @patch('gui.app.messagebox')
    def test_save_project_requirements_invalid_numeric(self, mock_messagebox):
        """Test _save_project_requirements with invalid numeric input."""
        self.app.entry_project_name.get = MagicMock(return_value="Test Invalid Numeric")
        self.app.entry_max_length.get = MagicMock(return_value="abc") # Invalid numeric
        self.app.entry_max_width.get = MagicMock(return_value="50")

        self.app._save_project_requirements()

        self.assertIsNone(self.app.project_requirements)
        mock_messagebox.showerror.assert_called_once_with("Validation Error", "Invalid input for Max Length. Must be a number.")

    @patch('gui.app.messagebox')
    def test_add_power_supply_block_valid_input(self, mock_messagebox):
        """Test _add_power_supply_block with valid inputs."""
        self.app.entry_psu_block_name.get = MagicMock(return_value="5V Rail")
        self.app.entry_psu_input_v.get = MagicMock(return_value="12.0")
        self.app.entry_psu_output_v.get = MagicMock(return_value="5.0")
        self.app.entry_psu_max_current.get = MagicMock(return_value="1.5")
        self.app.entry_psu_protection.get = MagicMock(return_value="short-circuit, over-voltage")
        
        # Mock listbox insert method
        self.app.listbox_psu_blocks.insert = MagicMock()
        # Mock entry delete methods
        self.app.entry_psu_block_name.delete = MagicMock()
        self.app.entry_psu_input_v.delete = MagicMock()
        self.app.entry_psu_output_v.delete = MagicMock()
        self.app.entry_psu_max_current.delete = MagicMock()
        self.app.entry_psu_protection.delete = MagicMock()

        self.app._add_power_supply_block()

        self.assertEqual(len(self.app.power_supply_requirements_list), 1)
        psu = self.app.power_supply_requirements_list[0]
        self.assertIsInstance(psu, PowerSupplyRequirements)
        self.assertEqual(psu.block_name, "5V Rail")
        self.assertEqual(psu.input_voltage_v, 12.0)
        self.assertEqual(psu.output_voltage_v, 5.0)
        self.assertEqual(psu.max_output_current_a, 1.5)
        self.assertEqual(psu.protection_features, ["short-circuit", "over-voltage"])
        
        mock_messagebox.showinfo.assert_called_once_with("Success", "Power Supply Block '5V Rail' added.")
        self.app.listbox_psu_blocks.insert.assert_called_once()
        # Check if entry fields were cleared
        self.app.entry_psu_block_name.delete.assert_called_once_with(0, tk.END)
        self.app.entry_psu_input_v.delete.assert_called_once_with(0, tk.END)
        # ... and so on for other PSU entry fields

    @patch('gui.app.messagebox')
    def test_add_power_supply_block_empty_block_name(self, mock_messagebox):
        """Test _add_power_supply_block with an empty block name."""
        self.app.entry_psu_block_name.get = MagicMock(return_value="")
        # Other fields don't matter
        self.app.entry_psu_input_v.get = MagicMock(return_value="12.0")


        self.app._add_power_supply_block()

        self.assertEqual(len(self.app.power_supply_requirements_list), 0)
        mock_messagebox.showerror.assert_called_once_with("Validation Error", "Power Supply Block Name cannot be empty.")

    @patch('gui.app.messagebox')
    def test_add_power_supply_block_invalid_mandatory_numeric(self, mock_messagebox):
        """Test _add_power_supply_block with invalid mandatory numeric input."""
        self.app.entry_psu_block_name.get = MagicMock(return_value="Test PSU")
        self.app.entry_psu_input_v.get = MagicMock(return_value="abc") # Invalid
        self.app.entry_psu_output_v.get = MagicMock(return_value="5.0")

        self.app._add_power_supply_block()

        self.assertEqual(len(self.app.power_supply_requirements_list), 0)
        mock_messagebox.showerror.assert_called_once_with("Validation Error", "Invalid Input Voltage. Must be a number.")

    @patch('gui.app.messagebox')
    def test_add_power_supply_block_empty_mandatory_numeric(self, mock_messagebox):
        """Test _add_power_supply_block with empty mandatory numeric input."""
        self.app.entry_psu_block_name.get = MagicMock(return_value="Test PSU Empty Numeric")
        self.app.entry_psu_input_v.get = MagicMock(return_value="12.0")
        self.app.entry_psu_output_v.get = MagicMock(return_value="") # Empty mandatory

        self.app._add_power_supply_block()
        self.assertEqual(len(self.app.power_supply_requirements_list), 0)
        mock_messagebox.showerror.assert_called_once_with("Validation Error", "Output Voltage is mandatory.")


    @patch('gui.app.messagebox')
    def test_finish_and_view_no_project_reqs(self, mock_messagebox):
        """Test _finish_and_view_requirements when project requirements are not saved."""
        self.app.project_requirements = None # Ensure it's None
        self.app._finish_and_view_requirements()
        mock_messagebox.showwarning.assert_called_once_with("Incomplete", "Project requirements have not been saved yet.")

    @patch('tkinter.Toplevel')
    @patch('tkinter.Text') # Patching the class
    @patch('gui.app.messagebox') # Also mock messagebox if it's used for warnings/info
    def test_finish_and_view_with_data(self, mock_messagebox, mock_text_class, mock_toplevel_class):
        """Test _finish_and_view_requirements with valid data."""
        # Setup valid project requirements
        self.app.project_requirements = ProjectRequirements(
            project_name="Final Test Project",
            max_length_mm=200.0,
            max_width_mm=150.0,
            target_cost_usd=50.0
        )
        # Optionally add a PSU
        psu1 = PowerSupplyRequirements(
            block_name="Main PSU", input_voltage_v=24.0, output_voltage_v=12.0,
            max_output_current_a=2.0, protection_features=["over-current"]
        )
        self.app.power_supply_requirements_list.append(psu1)

        # Mock the Text widget instance that will be created
        mock_text_instance = MagicMock()
        mock_text_class.return_value = mock_text_instance
        
        # Mock Toplevel instance
        mock_toplevel_instance = MagicMock()
        mock_toplevel_class.return_value = mock_toplevel_instance

        self.app._finish_and_view_requirements()

        mock_toplevel_class.assert_called_once_with(self.root_tk)
        mock_text_class.assert_called_once() # Check if Text widget was instantiated
        
        # Check if text was inserted into the Text widget
        # The actual content checking can be complex, so we check if insert was called.
        mock_text_instance.insert.assert_called_with(tk.END, unittest.mock.ANY)
        
        # Check that state was set to NORMAL then DISABLED
        calls = mock_text_instance.config.call_args_list
        self.assertIn(unittest.mock.call(state=tk.NORMAL), calls)
        self.assertIn(unittest.mock.call(state=tk.DISABLED), calls)

if __name__ == '__main__':
    unittest.main()
