# PCBGeniusAI

PCBGeniusAI is an innovative software project aiming to design Printed Circuit Boards (PCBs) automatically and intelligently. The system will interpret user requirements, generate schematics, perform PCB layouts, and produce complete technical project documentation, using Artificial Intelligence extensively throughout the process.

Our target audience includes electronic engineers, advanced hobbyists, hardware startups, and educational institutions looking for a smart assistant to accelerate and optimize the PCB design workflow.

## Current Status

This project is currently in a **very early, foundational stage of development**.

The existing functionality includes defining basic project-level and power supply block requirements. This can be done either via a command-line interface (CLI) or a new graphical user interface (GUI). The core Python data structures for capturing these initial requirements, along with basic GUI and CLI input mechanisms, have been implemented.

## Modules Implemented (So Far)

*   `core/requirements.py`: Defines Python dataclasses for representing project and power supply requirements.
*   `core/requirements_parser.py`: Provides a command-line interface (CLI) to interactively input these requirements.
*   `gui/app.py`: Provides a graphical user interface (GUI) using Tkinter for inputting project and power supply requirements.
*   `tests/test_requirements.py`: Contains unit tests for the requirements data structures and the CLI parser.
*   `tests/test_gui_app.py`: Contains unit tests for the GUI application logic.

## Getting Started / Usage

### Running the Application
To run the graphical user interface for requirements input:
1. Ensure you have Python 3.8+ installed (Tkinter is usually included).
2. Clone the repository (if applicable).
3. Navigate to the root directory of the project.
4. Execute the following command:
   ```bash
   python gui/app.py
   ```
This will launch the GUI, allowing you to input project and power supply block requirements.

(The original CLI for requirements input can still be run using `python core/requirements_parser.py` if preferred.)

## Future Goals (High Level)

The long-term vision for PCBGeniusAI includes the development of several advanced modules:

*   **AI-driven Requirements Interpretation**: Advanced NLP and potentially diagram parsing to understand complex user needs.
*   **Schematic Generation Service**: Automated creation of electronic schematics from interpreted requirements.
*   **Intelligent Component Selection**: AI models to select optimal components from a vast database based on specifications, cost, and availability.
*   **PCB Layout Automation Service**: AI-powered component placement and trace routing.
*   **Fabrication File Generation Service**: Automated generation of Gerbers, BOMs, and other manufacturing files.
*   **Technical Documentation Generation Service**: Automated creation of comprehensive project documentation.

## Architectural Documents

Detailed architectural plans, development roadmaps, technology stack proposals, data strategies, and AI model considerations are documented in various Markdown files within this repository (e.g., `SOFTWARE_ARCHITECTURE.md`, `DEVELOPMENT_PLAN.md`, `TECHNOLOGY_STACK.md`, etc.). These documents provide a more in-depth understanding of the project's vision, design, and future direction.

---

We appreciate your interest in PCBGeniusAI. Please note that this is an ambitious, long-term research and development project.
