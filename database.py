import csv
import json
import os
import sqlite3


DB_PATH = "fld_system_builder.db"

CSV_CATEGORY_MAP = {
    "data/pumps.csv": "pumps",
    "data/pipes.csv": "pipes",
    "data/devices.csv": "devices",
    "data/engines.csv": "engines",
    "data/motors.csv": "motors",
    "data/water_storage.csv": "water_storage",
    "data/fuel_storage.csv": "fuel_storage",
    "data/batteries.csv": "batteries",
    "data/generators.csv": "generators",
    "data/controls.csv": "controls",
    "data/sensors.csv": "sensors",
}

TABLE_FIELDS = {
    "pumps": ["name", "component_type", "unit_cost", "notes", "max_flow_gpm", "max_pressure_psi", "pump_type", "inlet_size_in", "outlet_size_in"],
    "pipes": [
    "name",
    "component_type",
    "unit_cost",
    "notes",
    "diameter_in",
    "internal_diameter_in",
    "wall_type",
    "pressure_rating_psi",
    "c_factor",
    "material"
],
    "devices": ["name", "component_type", "unit_cost", "notes", "flow_gpm", "required_pressure_psi", "nozzle_size", "throw_diameter_ft"],
    "engines": ["name", "component_type", "unit_cost", "notes", "fuel_type", "horsepower", "fuel_burn_gph"],
    "motors": ["name", "component_type", "unit_cost", "notes", "horsepower", "voltage", "phase", "efficiency"],
    "water_storage": ["name", "component_type", "unit_cost", "notes", "capacity_gallons", "storage_type"],
    "fuel_storage": ["name", "component_type", "unit_cost", "notes", "capacity_gallons", "fuel_type"],
    "batteries": ["name", "component_type", "unit_cost", "notes", "capacity_kwh", "usable_fraction"],
    "generators": ["name", "component_type", "unit_cost", "notes", "continuous_kw", "surge_kw", "fuel_type"],
    "controls": ["name", "component_type", "unit_cost", "notes", "control_type"],
    "sensors": ["name", "component_type", "unit_cost", "notes", "sensor_type"],
}


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def create_component_table(conn, category):
    fields = TABLE_FIELDS[category]
    column_defs = ["id INTEGER PRIMARY KEY AUTOINCREMENT"]

    for field in fields:
        column_defs.append(f"{field} TEXT")

    conn.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {category} (
            {", ".join(column_defs)}
        )
        """
    )


def get_table_columns(conn, table_name):
    rows = conn.execute(f"PRAGMA table_info({table_name})").fetchall()
    return [row["name"] for row in rows]


def add_column_if_missing(conn, table_name, column_name, column_def):
    columns = get_table_columns(conn, table_name)

    if column_name not in columns:
        conn.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_def}")


def create_saved_systems_table(conn):
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS saved_systems (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            input_json TEXT NOT NULL,
            result_json TEXT
        )
        """
    )

    add_column_if_missing(conn, "saved_systems", "project_name", "TEXT")
    add_column_if_missing(conn, "saved_systems", "version_label", "TEXT")
    add_column_if_missing(conn, "saved_systems", "revision_notes", "TEXT")
    add_column_if_missing(conn, "saved_systems", "status", "TEXT")
    add_column_if_missing(conn, "saved_systems", "client_name", "TEXT")
    add_column_if_missing(conn, "saved_systems", "property_name", "TEXT")
    add_column_if_missing(conn, "saved_systems", "site_notes", "TEXT")
    add_column_if_missing(conn, "saved_systems", "designer_notes", "TEXT")
    add_column_if_missing(conn, "saved_systems", "parent_id", "INTEGER")


def create_pump_curve_table(conn):
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS pump_curve_points (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pump_name TEXT NOT NULL,
            flow_gpm REAL NOT NULL,
            pressure_psi REAL NOT NULL,
            notes TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )


def init_database():
    conn = get_connection()

    for category in TABLE_FIELDS.keys():
        create_component_table(conn, category)

        for field in TABLE_FIELDS[category]:
            add_column_if_missing(conn, category, field, "TEXT")

    create_saved_systems_table(conn)
    create_pump_curve_table(conn)

    conn.commit()
    conn.close()


def count_rows(category):
    init_database()
    conn = get_connection()
    row = conn.execute(f"SELECT COUNT(*) AS count FROM {category}").fetchone()
    conn.close()
    return row["count"]


def read_csv_rows_from_file(path):
    if not os.path.exists(path):
        return []

    with open(path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)


def import_csv_category(category, path, replace=False):
    rows = read_csv_rows_from_file(path)
    conn = get_connection()

    if replace:
        conn.execute(f"DELETE FROM {category}")

    fields = TABLE_FIELDS[category]

    for row in rows:
        clean_row = {field: row.get(field, "") for field in fields}
        placeholders = ", ".join(["?"] * len(fields))
        columns = ", ".join(fields)

        conn.execute(
            f"""
            INSERT INTO {category} ({columns})
            VALUES ({placeholders})
            """,
            [clean_row[field] for field in fields]
        )

    conn.commit()
    conn.close()


def import_all_csv_if_empty():
    init_database()

    for path, category in CSV_CATEGORY_MAP.items():
        if count_rows(category) == 0:
            import_csv_category(category, path, replace=False)


def force_reimport_all_csv():
    init_database()

    for path, category in CSV_CATEGORY_MAP.items():
        import_csv_category(category, path, replace=True)


def rows_for_category(category):
    init_database()
    conn = get_connection()

    rows = conn.execute(f"SELECT * FROM {category} ORDER BY id ASC").fetchall()
    conn.close()

    output = []

    for row in rows:
        row_dict = {}
        for field in TABLE_FIELDS[category]:
            row_dict[field] = row[field]
        output.append(row_dict)

    return output


def rows_for_path(path):
    category = CSV_CATEGORY_MAP.get(path)

    if not category:
        raise ValueError(f"No database category mapped for path: {path}")

    return rows_for_category(category), TABLE_FIELDS[category]


def insert_row(category, row):
    init_database()
    fields = TABLE_FIELDS[category]
    clean_row = {field: row.get(field, "") for field in fields}

    placeholders = ", ".join(["?"] * len(fields))
    columns = ", ".join(fields)

    conn = get_connection()

    conn.execute(
        f"""
        INSERT INTO {category} ({columns})
        VALUES ({placeholders})
        """,
        [clean_row[field] for field in fields]
    )

    conn.commit()
    conn.close()


def add_row(category, row):
    insert_row(category, row)


def update_row_by_name(category, original_name, updated_row):
    init_database()
    fields = TABLE_FIELDS[category]
    set_clause = ", ".join([f"{field} = ?" for field in fields])
    values = [updated_row.get(field, "") for field in fields]
    values.append(original_name)

    conn = get_connection()

    conn.execute(
        f"""
        UPDATE {category}
        SET {set_clause}
        WHERE name = ?
        """,
        values
    )

    conn.commit()
    conn.close()


def delete_row_by_name(category, item_name):
    init_database()
    conn = get_connection()

    conn.execute(
        f"DELETE FROM {category} WHERE name = ?",
        (item_name,)
    )

    conn.commit()
    conn.close()


def write_rows_for_path(path, rows, fieldnames):
    init_database()
    category = CSV_CATEGORY_MAP.get(path)

    if not category:
        raise ValueError(f"No database category mapped for path: {path}")

    conn = get_connection()
    conn.execute(f"DELETE FROM {category}")

    fields = TABLE_FIELDS[category]

    for row in rows:
        clean_row = {field: row.get(field, "") for field in fields}
        placeholders = ", ".join(["?"] * len(fields))
        columns = ", ".join(fields)

        conn.execute(
            f"""
            INSERT INTO {category} ({columns})
            VALUES ({placeholders})
            """,
            [clean_row[field] for field in fields]
        )

    conn.commit()
    conn.close()


def make_json_safe(value):
    if value is None:
        return None

    if isinstance(value, (str, int, float, bool)):
        return value

    if isinstance(value, list):
        return [make_json_safe(item) for item in value]

    if isinstance(value, tuple):
        return [make_json_safe(item) for item in value]

    if isinstance(value, dict):
        return {str(key): make_json_safe(item) for key, item in value.items()}

    if hasattr(value, "__dict__"):
        return make_json_safe(value.__dict__)

    return str(value)


def save_system_design(
    name,
    input_data,
    result,
    project_name="",
    version_label="",
    revision_notes="",
    status="Draft",
    client_name="",
    property_name="",
    site_notes="",
    designer_notes="",
    parent_id=None
):
    init_database()

    input_json = json.dumps(make_json_safe(input_data), indent=2)
    result_json = json.dumps(make_json_safe(result), indent=2)

    if not project_name:
        project_name = name

    if not version_label:
        version_label = "V1"

    conn = get_connection()

    cursor = conn.execute(
        """
        INSERT INTO saved_systems (
            name,
            project_name,
            version_label,
            revision_notes,
            status,
            client_name,
            property_name,
            site_notes,
            designer_notes,
            parent_id,
            input_json,
            result_json
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            name,
            project_name,
            version_label,
            revision_notes,
            status,
            client_name,
            property_name,
            site_notes,
            designer_notes,
            parent_id,
            input_json,
            result_json
        )
    )

    conn.commit()
    saved_id = cursor.lastrowid
    conn.close()

    return saved_id


def list_saved_systems():
    init_database()
    conn = get_connection()

    rows = conn.execute(
        """
        SELECT
            id,
            name,
            project_name,
            version_label,
            status,
            client_name,
            property_name,
            created_at,
            parent_id
        FROM saved_systems
        ORDER BY id DESC
        """
    ).fetchall()

    conn.close()

    return [
        {
            "id": row["id"],
            "name": row["name"],
            "project_name": row["project_name"] or row["name"],
            "version_label": row["version_label"] or "",
            "status": row["status"] or "",
            "client_name": row["client_name"] or "",
            "property_name": row["property_name"] or "",
            "created_at": row["created_at"],
            "parent_id": row["parent_id"],
        }
        for row in rows
    ]


def get_saved_system(system_id):
    init_database()
    conn = get_connection()

    row = conn.execute(
        """
        SELECT *
        FROM saved_systems
        WHERE id = ?
        """,
        (system_id,)
    ).fetchone()

    conn.close()

    if not row:
        return None

    return {
        "id": row["id"],
        "name": row["name"],
        "project_name": row["project_name"] or row["name"],
        "version_label": row["version_label"] or "",
        "revision_notes": row["revision_notes"] or "",
        "status": row["status"] or "",
        "client_name": row["client_name"] or "",
        "property_name": row["property_name"] or "",
        "site_notes": row["site_notes"] or "",
        "designer_notes": row["designer_notes"] or "",
        "parent_id": row["parent_id"],
        "created_at": row["created_at"],
        "input_data": json.loads(row["input_json"]),
        "result": json.loads(row["result_json"]) if row["result_json"] else None,
        "input_json": row["input_json"],
        "result_json": row["result_json"],
    }


def delete_saved_system(system_id):
    init_database()
    conn = get_connection()

    conn.execute(
        "DELETE FROM saved_systems WHERE id = ?",
        (system_id,)
    )

    conn.commit()
    conn.close()


def add_pump_curve_point(pump_name, flow_gpm, pressure_psi, notes=""):
    init_database()
    conn = get_connection()

    conn.execute(
        """
        INSERT INTO pump_curve_points (pump_name, flow_gpm, pressure_psi, notes)
        VALUES (?, ?, ?, ?)
        """,
        (pump_name, float(flow_gpm), float(pressure_psi), notes)
    )

    conn.commit()
    conn.close()


def list_pump_curve_points(pump_name=None):
    init_database()
    conn = get_connection()

    if pump_name:
        rows = conn.execute(
            """
            SELECT id, pump_name, flow_gpm, pressure_psi, notes, created_at
            FROM pump_curve_points
            WHERE pump_name = ?
            ORDER BY flow_gpm ASC
            """,
            (pump_name,)
        ).fetchall()
    else:
        rows = conn.execute(
            """
            SELECT id, pump_name, flow_gpm, pressure_psi, notes, created_at
            FROM pump_curve_points
            ORDER BY pump_name ASC, flow_gpm ASC
            """
        ).fetchall()

    conn.close()

    return [
        {
            "id": row["id"],
            "pump_name": row["pump_name"],
            "flow_gpm": row["flow_gpm"],
            "pressure_psi": row["pressure_psi"],
            "notes": row["notes"] or "",
            "created_at": row["created_at"],
        }
        for row in rows
    ]


def delete_pump_curve_point(point_id):
    init_database()
    conn = get_connection()

    conn.execute(
        "DELETE FROM pump_curve_points WHERE id = ?",
        (point_id,)
    )

    conn.commit()
    conn.close()


def clear_pump_curve_points(pump_name):
    init_database()
    conn = get_connection()

    conn.execute(
        "DELETE FROM pump_curve_points WHERE pump_name = ?",
        (pump_name,)
    )

    conn.commit()
    conn.close()