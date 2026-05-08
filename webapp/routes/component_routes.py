from flask import Blueprint, render_template

component_bp = Blueprint("components", __name__)

COMPONENT_LIBRARY = [
    {
        "key": "pump_package_light",
        "item": "GX390-Class Pump Package",
        "unit_cost": 4500,
        "notes": "Light-duty residential wildfire pump platform"
    }
]

@component_bp.route("/components")
def components():
    return render_template("components.html", components=COMPONENT_LIBRARY)
