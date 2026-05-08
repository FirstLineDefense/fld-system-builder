from flask import Blueprint, render_template

components_bp = Blueprint("components", __name__)

COMPONENT_LIBRARY = [
    {
        "key": "pump_package_light",
        "item": "GX390-Class Pump Package",
        "unit_cost": 4500,
        "notes": "Light-duty residential wildfire pump platform"
    }
]

@components_bp.route("/components")
def components():
    try:
        return render_template("components.html", components=COMPONENT_LIBRARY)
    except Exception as e:
        return f"Components error: {str(e)}", 200
