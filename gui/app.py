"""
Main application file for the PCBGeniusAI GUI.
This file will contain the main Tkinter application setup and core UI logic.
"""
import tkinter as tk
from tkinter import ttk, messagebox # Added messagebox
from core.requirements import ProjectRequirements, PowerSupplyRequirements

class RequirementsApp:
    """
    The main application class for the PCBGeniusAI Requirements Input GUI.
    This class handles the creation and layout of the main window and its widgets.
    """
    def __init__(self, root_window):
        """
        Initializes the RequirementsApp.

        Args:
            root_window (tk.Tk): The main Tkinter window.
        """
        self.root = root_window
        self.root.title("PCBGeniusAI - Requirements Input")

        # --- Menu Bar ---
        menubar = tk.Menu(self.root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        self.root.config(menu=menubar)
        
        self.root.minsize(550, 650) # Adjusted minsize for more content

        # Store collected requirements
        self.project_requirements: ProjectRequirements = None # type: ignore
        self.power_supply_requirements_list: list = []

        # Main frame for organization
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Welcome label moved into main_frame
        welcome_label = ttk.Label(
            main_frame,
            text="Welcome to PCBGeniusAI Requirements Input",
            font=("Arial", 16, "bold") # Made it a bit more prominent
        )
        welcome_label.pack(pady=10)

        # --- Project Requirements Section ---
        project_req_frame = ttk.LabelFrame(main_frame, text="Project Requirements", padding="10")
        project_req_frame.pack(fill=tk.X, padx=5, pady=5) # Use pack for the frame itself

        # Configure columns for the grid within project_req_frame
        project_req_frame.columnconfigure(1, weight=1) # Make entry column expandable

        self.entry_project_name = self._create_label_entry(
            project_req_frame, "Project Name:", 0
        )
        self.entry_max_length = self._create_label_entry(
            project_req_frame, "Max Length (mm):", 1
        )
        self.entry_max_width = self._create_label_entry(
            project_req_frame, "Max Width (mm):", 2
        )
        self.entry_target_cost = self._create_label_entry(
            project_req_frame, "Target Cost (USD):", 3
        )
        
        # --- Buttons Section ---
        buttons_frame = ttk.Frame(main_frame, padding="5")
        buttons_frame.pack(fill=tk.X, pady=5)

        self.btn_save_project_reqs = ttk.Button(
            buttons_frame,
            text="Save Project Requirements",
            command=self._save_project_requirements # Updated command
        )
        self.btn_save_project_reqs.pack(side=tk.LEFT, padx=5)

        # --- Power Supply Requirements Section ---
        psu_req_frame = ttk.LabelFrame(main_frame, text="Power Supply Block Details", padding="10")
        psu_req_frame.pack(fill=tk.X, padx=5, pady=5)
        psu_req_frame.columnconfigure(1, weight=1) # Make entry column expandable

        self.entry_psu_block_name = self._create_label_entry(
            psu_req_frame, "Block Name:", 0
        )
        self.entry_psu_input_v = self._create_label_entry(
            psu_req_frame, "Input Voltage (V):", 1
        )
        self.entry_psu_output_v = self._create_label_entry(
            psu_req_frame, "Output Voltage (V):", 2
        )
        self.entry_psu_max_current = self._create_label_entry(
            psu_req_frame, "Max Output Current (A):", 3
        )
        self.entry_psu_protection = self._create_label_entry(
            psu_req_frame, "Protection Features (comma-sep):", 4
        )

        self.btn_add_psu = ttk.Button(
            psu_req_frame, # Placed inside the PSU frame for grouping
            text="Add Power Supply Block",
            command=self._add_power_supply_block # Updated command
        )
        # Place button spanning across columns, below the entries
        self.btn_add_psu.grid(row=5, column=0, columnspan=2, pady=10, padx=5)


        # --- Added Power Supply Blocks Display Area ---
        added_psu_frame = ttk.LabelFrame(main_frame, text="Added Power Supply Blocks", padding="10")
        added_psu_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.listbox_psu_blocks = tk.Listbox(added_psu_frame, height=5)
        self.listbox_psu_blocks.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=5, padx=(5,0))

        psu_scrollbar = ttk.Scrollbar(added_psu_frame, orient=tk.VERTICAL, command=self.listbox_psu_blocks.yview)
        psu_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=5, padx=(0,5))
        self.listbox_psu_blocks.config(yscrollcommand=psu_scrollbar.set)
        
        # --- Final Button ---
        self.btn_finish = ttk.Button(
            main_frame, # Placed in main_frame, below other sections
            text="Finish & View All Requirements",
            command=self._finish_and_view_requirements # Updated command
        )
        self.btn_finish.pack(pady=10, padx=5, side=tk.BOTTOM)


    def _create_label_entry(self, parent, label_text, row, col_label=0, col_entry=1) -> ttk.Entry:
        """
        Helper method to create a ttk.Label and ttk.Entry pair and grid them.

        Args:
            parent: The parent widget.
            label_text (str): The text for the label.
            row (int): The grid row for placement.
            col_label (int): The grid column for the label.
            col_entry (int): The grid column for the entry.

        Returns:
            ttk.Entry: The created Entry widget.
        """
        label = ttk.Label(parent, text=label_text)
        label.grid(row=row, column=col_label, padx=5, pady=5, sticky=tk.W)
        
        entry = ttk.Entry(parent, width=40) # Increased width a bit
        entry.grid(row=row, column=col_entry, padx=5, pady=5, sticky=tk.EW)
        return entry

    def _save_project_requirements(self):
        """
        Validates and saves the project requirements from the input fields.
        """
        project_name = self.entry_project_name.get().strip()
        if not project_name:
            messagebox.showerror("Validation Error", "Project Name cannot be empty.")
            return

        max_length_str = self.entry_max_length.get().strip()
        max_width_str = self.entry_max_width.get().strip()
        target_cost_str = self.entry_target_cost.get().strip()

        max_length_mm = None
        if max_length_str:
            try:
                max_length_mm = float(max_length_str)
            except ValueError:
                messagebox.showerror("Validation Error", "Invalid input for Max Length. Must be a number.")
                return
        
        max_width_mm = None
        if max_width_str:
            try:
                max_width_mm = float(max_width_str)
            except ValueError:
                messagebox.showerror("Validation Error", "Invalid input for Max Width. Must be a number.")
                return

        target_cost_usd = None
        if target_cost_str:
            try:
                target_cost_usd = float(target_cost_str)
            except ValueError:
                messagebox.showerror("Validation Error", "Invalid input for Target Cost. Must be a number.")
                return
        
        self.project_requirements = ProjectRequirements(
            project_name=project_name,
            max_length_mm=max_length_mm,
            max_width_mm=max_width_mm,
            target_cost_usd=target_cost_usd
        )
        messagebox.showinfo("Success", "Project Requirements saved.")
        # Optionally disable fields or change button state
        # For example, disable the save button and entry fields:
        # self.btn_save_project_reqs.config(state=tk.DISABLED)
        # for entry in [self.entry_project_name, self.entry_max_length, self.entry_max_width, self.entry_target_cost]:
        #     entry.config(state=tk.DISABLED)

    def _add_power_supply_block(self):
        """
        Validates and adds a power supply block from input fields to the list.
        """
        block_name = self.entry_psu_block_name.get().strip()
        if not block_name:
            messagebox.showerror("Validation Error", "Power Supply Block Name cannot be empty.")
            return

        input_v_str = self.entry_psu_input_v.get().strip()
        output_v_str = self.entry_psu_output_v.get().strip()
        max_current_str = self.entry_psu_max_current.get().strip()
        protection_str = self.entry_psu_protection.get().strip()

        if not input_v_str:
            messagebox.showerror("Validation Error", "Input Voltage is mandatory.")
            return
        try:
            input_v = float(input_v_str)
        except ValueError:
            messagebox.showerror("Validation Error", "Invalid Input Voltage. Must be a number.")
            return

        if not output_v_str:
            messagebox.showerror("Validation Error", "Output Voltage is mandatory.")
            return
        try:
            output_v = float(output_v_str)
        except ValueError:
            messagebox.showerror("Validation Error", "Invalid Output Voltage. Must be a number.")
            return

        if not max_current_str:
            messagebox.showerror("Validation Error", "Max Output Current is mandatory.")
            return
        try:
            max_current = float(max_current_str)
        except ValueError:
            messagebox.showerror("Validation Error", "Invalid Max Output Current. Must be a number.")
            return
            
        protection_features = [f.strip() for f in protection_str.split(',') if f.strip()]

        psu = PowerSupplyRequirements(
            block_name=block_name,
            input_voltage_v=input_v,
            output_voltage_v=output_v,
            max_output_current_a=max_current,
            protection_features=protection_features
        )
        self.power_supply_requirements_list.append(psu)
        
        # Update listbox
        # For simplicity, just adding block_name. Could be a more detailed string.
        self.listbox_psu_blocks.insert(tk.END, f"{psu.block_name} (In: {psu.input_voltage_v}V, Out: {psu.output_voltage_v}V, {psu.max_output_current_a}A)")

        # Clear PSU entry fields
        self.entry_psu_block_name.delete(0, tk.END)
        self.entry_psu_input_v.delete(0, tk.END)
        self.entry_psu_output_v.delete(0, tk.END)
        self.entry_psu_max_current.delete(0, tk.END)
        self.entry_psu_protection.delete(0, tk.END)
        
        messagebox.showinfo("Success", f"Power Supply Block '{block_name}' added.")

    def _finish_and_view_requirements(self):
        """
        Displays all collected requirements in a new Toplevel window.
        """
        if not self.project_requirements:
            messagebox.showwarning("Incomplete", "Project requirements have not been saved yet.")
            return

        display_window = tk.Toplevel(self.root)
        display_window.title("Collected Requirements")
        display_window.minsize(400, 300)

        text_frame = ttk.Frame(display_window, padding="5")
        text_frame.pack(fill=tk.BOTH, expand=True)

        text_widget = tk.Text(text_frame, wrap=tk.WORD, height=25, width=80, relief=tk.SUNKEN, borderwidth=1)
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text_widget.yview)
        text_widget.config(yscrollcommand=scrollbar.set)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Build the formatted string
        output_string = "--- Project Requirements ---\n"
        pr = self.project_requirements
        output_string += f"Project Name: {pr.project_name}\n"
        output_string += f"Max Length (mm): {pr.max_length_mm if pr.max_length_mm is not None else 'N/A'}\n"
        output_string += f"Max Width (mm): {pr.max_width_mm if pr.max_width_mm is not None else 'N/A'}\n"
        output_string += f"Target Cost (USD): {pr.target_cost_usd if pr.target_cost_usd is not None else 'N/A'}\n"

        output_string += f"\n--- Power Supply Blocks ({len(self.power_supply_requirements_list)} entries) ---\n"
        if not self.power_supply_requirements_list:
            output_string += "No power supply blocks added.\n"
        else:
            for i, psu in enumerate(self.power_supply_requirements_list, 1):
                output_string += f"\n{i}. Block Name: {psu.block_name}\n"
                output_string += f"   Input Voltage (V): {psu.input_voltage_v}\n"
                output_string += f"   Output Voltage (V): {psu.output_voltage_v}\n"
                output_string += f"   Max Output Current (A): {psu.max_output_current_a}\n"
                protection_str = ", ".join(psu.protection_features) if psu.protection_features else "None"
                output_string += f"   Protection Features: {protection_str}\n"
        
        text_widget.config(state=tk.NORMAL) # Enable writing to text widget
        text_widget.delete('1.0', tk.END) # Clear previous content
        text_widget.insert(tk.END, output_string)
        text_widget.config(state=tk.DISABLED) # Make read-only

        # Optional: print to console for debugging
        print("\n--- Displaying Requirements ---")
        print(output_string)
        # No need for a messagebox here as the new window is the confirmation.
        # messagebox.showinfo("Success", "Requirements displayed.")


if __name__ == '__main__':
    # Create the root Tkinter window
    root = tk.Tk()

    # Instantiate the RequirementsApp
    app = RequirementsApp(root)

    # Start the Tkinter event loop
    root.mainloop()
