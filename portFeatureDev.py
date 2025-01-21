
# Software Composition Classes
class SoftwareComposition:
    """
    Represents a Software Composition in AUTOSAR, containing multiple Software Components.
    """
    def __init__(self, name):
        self.name = name
        self.software_components = []  # List to hold SoftwareComponent objects
        self.interfaces = []  # Centralized list of Interface objects
        print(f"The composition '{self.name}' has been succefuly created.")  # Message displayed after creation

    def add_software_component(self, swc):
        """
        Adds a Software Component to the composition.
        Ensures no duplicate component names exist.
        """
        if any(component.name == swc.name for component in self.software_components):
            raise ValueError(f"A SoftwareComponent with the name '{swc.name}' already exists.")
        self.software_components.append(swc)

    def list_software_components(self):
        """Returns a list of the names of all Software Components in the composition."""
        print("the SWCs associated to this composition are :")
        for component in self.software_components:
            print(component.name)

    def listSWC(self):
        """Returns a list of the names of all Software Components in the composition."""
        ls = [component.name for component in self.software_components]
        return ls
    def selectswc(self,n):
        for sw in  self.software_components:
            if sw.name == n:
                return sw
        return None


class SoftwareComponent:
    """
    Represents a Software Component in AUTOSAR, containing ports, runnables, and interfaces.
    """
    def __init__(self, name, component_type):
        self.name = name
        self.component_type = component_type  # Type of the component (e.g., "Sensor", "Controller")
        self.runnables = []  # List of Runnable objects
        self.ports = {}  # Dictionary to map port names to Port objects for efficient lookup
        print(f"The software component '{self.name}' has been succefuly created.")  # Message displayed after creation
    def add_port(self, port):
        """Adds a Port to the component."""
        if not isinstance(port, Port):
            raise TypeError("Expected a Port object.")
        if port.pname in self.ports:
            raise ValueError(f"Port with the name '{port.pname}' already exists in component '{self.name}'.")
        self.ports[port.pname] = port

    def add_runnable(self, runnable):
        """Adds a Runnable to the component."""
        if not isinstance(runnable, Runnable):
            raise TypeError("Expected a Runnable object.")
        if any(r.name == runnable.name for r in self.runnables):
            raise ValueError(f"Runnable with the name '{runnable.name}' already exists in component '{self.name}'.")
        self.runnables.append(runnable)
    @classmethod
    def copy(cls, other):
        """Creates a new SoftwareComponent by copying an existing one."""
        if not isinstance(other, cls):
            raise TypeError("Expected a SoftwareComponent object to copy.")
        
        # Create a new instance with the same name and type
        new_instance = cls(other.name, other.component_type)
        
        # Deep copy of ports
        new_instance.ports = {name: Port(port.name, port.port_type) for name, port in other.ports.items()}
        
        # Deep copy of runnables
        new_instance.runnables = [Runnable(r.name, r.trigger, r.period) for r in other.runnables]
        
        return new_instance

class Runnable:
    """
    Represents a Runnable, which is a task or function executed by the component.
    """
    def __init__(self, name, type,period= None):
        self.name = name
        self.type = type.lower()  # Normalize to lowercase for consistency
        if self.type == "periodic":
            self.period = input("Enter the period of the runnable :")
        else:
            self.period = None

           

class Port:
    """
    Represents a Port for communication in AUTOSAR.
    """
    def __init__(self, name, port_type):
        self.pname = name
        self.port_type = port_type  # Port type: "sender" or "receiver"
        print(f"Port '{self.pname}' has been succefuly created")

def display_architecture(composition):
    """
    
    Displays the full architecture of a Software Composition"""
    print(f"Composition: '{composition.name}'")
    print("    SWCs associés:")
    for index, component in enumerate(composition.software_components, start=1):
        print(f"    {index}- Nom: '{component.name}', Type: '{component.component_type}'")
        for runn in component.runnables:
                print(f"Runnable Name: {runn.name}, run_type: {runn.type}" + 
      (f", run_period: {runn.period}" if runn.type == "periodic" else ""))
        for port_obj in component.ports.items():
            print(f"        Port Name: {port_obj.pname}, Port Type: {port_obj.port_type}")
            


# Interactive Configuration Function
def interactive_configuration():
    print(" ")
    print(" ")
    print(" ")
    print("Welcome to the Software Configuration Tool!")
#############tool Menu ##########
compo21 = SoftwareComposition("Compo21")
swc1 = SoftwareComponent("swc1","application")
swc2 = SoftwareComponent("swc2","application")
swc3 = SoftwareComponent("swc3","Sensor")
compo21.add_software_component(swc1)
compo21.add_software_component(swc2)
compo21.add_software_component(swc3)

while(True):
    print("              MENU           ")
    print("1-- Create software composition ")
    print("2-- Create software component")
    print("3-- Create Port")
    print("4-- display the architecture")
    print("6-- Create a runnable")
    print("5-- exit")
    choice = input("Enter your choice :")

    if choice == "1":
        #composition_name = input("Enter the name for your software composition: ")
        composition = compo21
    elif choice == "2":
        SoftwareComponent_name,swc_type = input("Enter the name for your SWC and type (separated by space) ").split()
        swc = SoftwareComponent(SoftwareComponent_name,swc_type)
        composition.add_software_component(swc)
        composition.list_software_components()
    elif choice == "3":
        composition.list_software_components()
        thisSWC = input("Choose the swc that you want to associate to a port :")
        myswc = composition.selectswc(thisSWC)
        PortName,portType = input("Enter the name of the port and its type (space)").split()
        port = Port(PortName,portType)
        myswc.add_port(port)
        print(f"\nSoftware Component '{myswc.name}' Details:")
        print(f"  Type: {myswc.component_type}")
        print(f"  Ports: ")
        for port_name, port_obj in myswc.ports.items():
            print(f"    Port Name: {port_obj.pname}, Port Type: {port_obj.port_type}")
        
    elif choice == "4":
        display_architecture(composition)
    elif choice == "5":
        break
    elif choice == "6":
        composition.list_software_components()
        thisSWC = input("Choose the swc that you want to associate to a runnable :")
        myswc = composition.selectswc(thisSWC)
        run_name,run_type = input("Enter the name of the runnable and its type ").split()
        runnab = Runnable(run_name,run_type)
        myswc.add_runnable(runnab)
        print(f"\nSoftware Component '{myswc.name}' Details:")
        print(f"  Type: {myswc.component_type}")
        print(f"  Ports: ")
        for port_name, port_obj in myswc.ports.items():
            print(f"    Port Name: {port_obj.pname}, Port Type: {port_obj.port_type}")
        for runname, runtype, run_period in myswc.ports.items():
            if run_period == None :
                print(f"    Runnable Name: {runname.name}, Runnable type: {runname.type}")
            else:
                print(f"    Runnable Name: {runname.name}, Runnable type: {runname.type}, Runnable period:{runname.period} ")
        








# Run the interactive tool
interactive_configuration()
