"""
Defines data structures for representing an electronic schematic.
"""
from dataclasses import dataclass, field
from typing import List, Dict, Set

@dataclass(frozen=True)
class Pin:
    """
    Represents a single, unique pin on a component.
    Using frozen=True to make Pin objects hashable so they can be added to sets.
    """
    component_ref_des: str  # Reference designator of the parent component (e.g., "U1")
    pin_name: str           # Name or number of the pin (e.g., "VIN", "GND", "1", "2")

@dataclass
class Component:
    """Represents an instance of an electronic component in the schematic."""
    reference_designator: str  # e.g., "U1", "C1", "R1"
    part_number: str           # e.g., "LM7805", "10uF_CAP"
    description: str           # e.g., "5V Linear Regulator", "Decoupling Capacitor"

    def get_pin(self, pin_name: str) -> Pin:
        """Helper method to create a Pin instance associated with this component."""
        return Pin(component_ref_des=self.reference_designator, pin_name=pin_name)

@dataclass
class Net:
    """Represents a connection (a net) between multiple component pins."""
    name: str
    pins: Set[Pin] = field(default_factory=set)

    def add_connection(self, pin: Pin):
        """Adds a component pin to this net."""
        self.pins.add(pin)

@dataclass
class Schematic:
    """Represents the entire electronic schematic, containing all components and nets."""
    components: List[Component] = field(default_factory=list)
    nets: List[Net] = field(default_factory=list)

    def add_component(self, component: Component):
        """Adds a component to the schematic."""
        self.components.append(component)

    def add_net(self, net: Net):
        """Adds a net to the schematic."""
        self.nets.append(net)

    def find_net(self, name: str) -> Net or None:
        """Finds a net by its name."""
        for net in self.nets:
            if net.name == name:
                return net
        return None

    def get_or_create_net(self, name: str) -> Net:
        """
        Returns an existing net with the given name or creates, adds, and returns a new one.
        """
        net = self.find_net(name)
        if net is None:
            net = Net(name=name)
            self.add_net(net)
        return net