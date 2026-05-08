from dataclasses import dataclass


@dataclass
class Component:
    name: str
    component_type: str
    unit_cost: float = 0.0
    notes: str = ""


@dataclass
class Pump(Component):
    max_flow_gpm: float = 0.0
    max_pressure_psi: float = 0.0
    pump_type: str = ""
    inlet_size_in: float = 0.0
    outlet_size_in: float = 0.0


@dataclass
class Engine(Component):
    fuel_type: str = ""
    horsepower: float = 0.0
    fuel_burn_gph: float = 0.0


@dataclass
class Motor(Component):
    horsepower: float = 0.0
    voltage: float = 0.0
    phase: str = ""
    efficiency: float = 0.0


@dataclass
class Pipe(Component):
    diameter_in: float = 0.0
    c_factor: float = 150
    material: str = "PVC"


@dataclass
class Fitting(Component):
    size_in: float = 0.0
    fitting_type: str = ""
    equivalent_length_ft: float = 0.0


@dataclass
class Valve(Component):
    size_in: float = 0.0
    valve_type: str = ""


@dataclass
class TerminalDevice(Component):
    flow_gpm: float = 0.0
    required_pressure_psi: float = 0.0
    nozzle_size: str = ""
    throw_diameter_ft: float = 0.0


@dataclass
class WaterStorage(Component):
    capacity_gallons: float = 0.0
    storage_type: str = ""


@dataclass
class FuelStorage(Component):
    capacity_gallons: float = 0.0
    fuel_type: str = ""


@dataclass
class Battery(Component):
    capacity_kwh: float = 0.0
    usable_fraction: float = 0.8


@dataclass
class Generator(Component):
    continuous_kw: float = 0.0
    surge_kw: float = 0.0
    fuel_type: str = ""


@dataclass
class Control(Component):
    control_type: str = ""


@dataclass
class Sensor(Component):
    sensor_type: str = ""