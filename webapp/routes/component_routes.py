from flask import Blueprint, render_template

from data.components import COMPONENT_LIBRARY

component_bp = Blueprint("components", __name__)


@component_bp.route("/components")
def components():
    return render_template("components.html", components=COMPONENT_LIBRARY)
