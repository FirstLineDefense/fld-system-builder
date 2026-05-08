from database import rows_for_path, import_all_csv_if_empty


def safe_float(value, default=0):
    try:
        if value is None or value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


class Component:

    def __init__(self, name, component_type, unit_cost, notes):
        self.name = name
        self.component_type = component_type
        self.unit_cost = safe_float(unit_cost)
        self.notes = notes


class Pump(Component):

    def __init__(
        self,
        name,
        component_type,
        unit_cost,
        notes,
        max_flow_gpm,
        max_pressure_psi,
        pump_type,
        inlet_size_in,
        outlet_size_in
    ):
        super().__init__(name, component_type, unit_cost, notes)
        self.max_flow_gpm = safe_float(max_flow_gpm)
        self.max_pressure_psi = safe_float(max_pressure_psi)
        self.pump_type = pump_type
        self.inlet_size_in = safe_float(inlet_size_in)
        self.outlet_size_in = safe_float(outlet_size_in)


class Pipe(Component):

    def __init__(
        self,
        name,
        component_type,
        unit_cost,
        notes,
        diameter_in,
        c_factor,
        material,
        internal_diameter_in=None,
        wall_type="Sch40",
        pressure_rating_psi=0
    ):
        super().__init__(name, component_type, unit_cost, notes)

        self.diameter_in = safe_float(diameter_in)

        self.c_factor = safe_float(c_factor, 150)

        self.material = material

        self.wall_type = wall_type

        self.pressure_rating_psi = safe_float(
            pressure_rating_psi,
            0
        )

        if internal_diameter_in in [None, ""]:
            self.internal_diameter_in = self.diameter_in
        else:
            self.internal_diameter_in = safe_float(
                internal_diameter_in
            )


class Device(Component):

    def __init__(
        self,
        name,
        component_type,
        unit_cost,
        notes,
        flow_gpm,
        required_pressure_psi,
        nozzle_size,
        throw_diameter_ft
    ):
        super().__init__(name, component_type, unit_cost, notes)
        self.flow_gpm = safe_float(flow_gpm)
        self.required_pressure_psi = safe_float(required_pressure_psi)
        self.nozzle_size = nozzle_size
        self.throw_diameter_ft = safe_float(throw_diameter_ft)


class Engine(Component):

    def __init__(
        self,
        name,
        component_type,
        unit_cost,
        notes,
        fuel_type,
        horsepower,
        fuel_burn_gph
    ):
        super().__init__(name, component_type, unit_cost, notes)
        self.fuel_type = fuel_type
        self.horsepower = safe_float(horsepower)
        self.fuel_burn_gph = safe_float(fuel_burn_gph)


class Motor(Component):

    def __init__(
        self,
        name,
        component_type,
        unit_cost,
        notes,
        horsepower,
        voltage,
        phase,
        efficiency
    ):
        super().__init__(name, component_type, unit_cost, notes)
        self.horsepower = safe_float(horsepower)
        self.voltage = safe_float(voltage)
        self.phase = phase
        self.efficiency = safe_float(efficiency, 0.9)


class WaterStorage(Component):

    def __init__(
        self,
        name,
        component_type,
        unit_cost,
        notes,
        capacity_gallons,
        storage_type
    ):
        super().__init__(name, component_type, unit_cost, notes)
        self.capacity_gallons = safe_float(capacity_gallons)
        self.storage_type = storage_type


class FuelStorage(Component):

    def __init__(
        self,
        name,
        component_type,
        unit_cost,
        notes,
        capacity_gallons,
        fuel_type
    ):
        super().__init__(name, component_type, unit_cost, notes)
        self.capacity_gallons = safe_float(capacity_gallons)
        self.fuel_type = fuel_type


class Battery(Component):

    def __init__(
        self,
        name,
        component_type,
        unit_cost,
        notes,
        capacity_kwh,
        usable_fraction
    ):
        super().__init__(name, component_type, unit_cost, notes)
        self.capacity_kwh = safe_float(capacity_kwh)
        self.usable_fraction = safe_float(usable_fraction, 0.8)


class Generator(Component):

    def __init__(
        self,
        name,
        component_type,
        unit_cost,
        notes,
        continuous_kw,
        surge_kw,
        fuel_type
    ):
        super().__init__(name, component_type, unit_cost, notes)
        self.continuous_kw = safe_float(continuous_kw)
        self.surge_kw = safe_float(surge_kw)
        self.fuel_type = fuel_type


class Control(Component):

    def __init__(
        self,
        name,
        component_type,
        unit_cost,
        notes,
        control_type
    ):
        super().__init__(name, component_type, unit_cost, notes)
        self.control_type = control_type


class Sensor(Component):

    def __init__(
        self,
        name,
        component_type,
        unit_cost,
        notes,
        sensor_type
    ):
        super().__init__(name, component_type, unit_cost, notes)
        self.sensor_type = sensor_type


def load_csv_rows(path):
    rows, _ = rows_for_path(path)
    return rows


def load_pumps():
    rows = load_csv_rows("data/pumps.csv")
    pumps = []

    for row in rows:
        pumps.append(
            Pump(
                row.get("name", ""),
                row.get("component_type", "pump"),
                row.get("unit_cost", 0),
                row.get("notes", ""),
                row.get("max_flow_gpm", 0),
                row.get("max_pressure_psi", 0),
                row.get("pump_type", ""),
                row.get("inlet_size_in", 0),
                row.get("outlet_size_in", 0),
            )
        )

    return pumps


def load_pipes():
    rows = load_csv_rows("data/pipes.csv")

    pipes = []

    for row in rows:
        pipes.append(
            Pipe(
                row.get("name", ""),
                row.get("component_type", "pipe"),
                row.get("unit_cost", 0),
                row.get("notes", ""),
                row.get("diameter_in", 0),
                row.get("c_factor", 150),
                row.get("material", ""),
                row.get("internal_diameter_in", ""),
                row.get("wall_type", "Sch40"),
                row.get("pressure_rating_psi", 0),
            )
        )

    return pipes


def load_devices():
    rows = load_csv_rows("data/devices.csv")
    devices = []

    for row in rows:
        devices.append(
            Device(
                row.get("name", ""),
                row.get("component_type", "terminal"),
                row.get("unit_cost", 0),
                row.get("notes", ""),
                row.get("flow_gpm", 0),
                row.get("required_pressure_psi", 0),
                row.get("nozzle_size", ""),
                row.get("throw_diameter_ft", 0),
            )
        )

    return devices


def load_engines():
    rows = load_csv_rows("data/engines.csv")
    engines = []

    for row in rows:
        engines.append(
            Engine(
                row.get("name", ""),
                row.get("component_type", "engine"),
                row.get("unit_cost", 0),
                row.get("notes", ""),
                row.get("fuel_type", ""),
                row.get("horsepower", 0),
                row.get("fuel_burn_gph", 0),
            )
        )

    return engines


def load_motors():
    rows = load_csv_rows("data/motors.csv")
    motors = []

    for row in rows:
        motors.append(
            Motor(
                row.get("name", ""),
                row.get("component_type", "motor"),
                row.get("unit_cost", 0),
                row.get("notes", ""),
                row.get("horsepower", 0),
                row.get("voltage", 0),
                row.get("phase", ""),
                row.get("efficiency", 0.9),
            )
        )

    return motors


def load_water_storage():
    rows = load_csv_rows("data/water_storage.csv")
    storage = []

    for row in rows:
        storage.append(
            WaterStorage(
                row.get("name", ""),
                row.get("component_type", "water_storage"),
                row.get("unit_cost", 0),
                row.get("notes", ""),
                row.get("capacity_gallons", 0),
                row.get("storage_type", ""),
            )
        )

    return storage


def load_fuel_storage():
    rows = load_csv_rows("data/fuel_storage.csv")
    storage = []

    for row in rows:
        storage.append(
            FuelStorage(
                row.get("name", ""),
                row.get("component_type", "fuel_storage"),
                row.get("unit_cost", 0),
                row.get("notes", ""),
                row.get("capacity_gallons", 0),
                row.get("fuel_type", ""),
            )
        )

    return storage


def load_batteries():
    rows = load_csv_rows("data/batteries.csv")
    batteries = []

    for row in rows:
        batteries.append(
            Battery(
                row.get("name", ""),
                row.get("component_type", "battery"),
                row.get("unit_cost", 0),
                row.get("notes", ""),
                row.get("capacity_kwh", 0),
                row.get("usable_fraction", 0.8),
            )
        )

    return batteries


def load_generators():
    rows = load_csv_rows("data/generators.csv")
    generators = []

    for row in rows:
        generators.append(
            Generator(
                row.get("name", ""),
                row.get("component_type", "generator"),
                row.get("unit_cost", 0),
                row.get("notes", ""),
                row.get("continuous_kw", 0),
                row.get("surge_kw", 0),
                row.get("fuel_type", ""),
            )
        )

    return generators


def load_controls():
    rows = load_csv_rows("data/controls.csv")
    controls = []

    for row in rows:
        controls.append(
            Control(
                row.get("name", ""),
                row.get("component_type", "control"),
                row.get("unit_cost", 0),
                row.get("notes", ""),
                row.get("control_type", ""),
            )
        )

    return controls


def load_sensors():
    rows = load_csv_rows("data/sensors.csv")
    sensors = []

    for row in rows:
        sensors.append(
            Sensor(
                row.get("name", ""),
                row.get("component_type", "sensor"),
                row.get("unit_cost", 0),
                row.get("notes", ""),
                row.get("sensor_type", ""),
            )
        )

    return sensors


def get_component_library():
    import_all_csv_if_empty()

    return {
        "pumps": load_pumps(),
        "pipes": load_pipes(),
        "devices": load_devices(),
        "engines": load_engines(),
        "motors": load_motors(),
        "water_storage": load_water_storage(),
        "fuel_storage": load_fuel_storage(),
        "batteries": load_batteries(),
        "generators": load_generators(),
        "controls": load_controls(),
        "sensors": load_sensors(),
    }