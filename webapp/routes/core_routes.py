from flask import Blueprint, render_template

core_bp = Blueprint("core", __name__)


@core_bp.route("/")
def dashboard():
    return render_template("dashboard.html")


@core_bp.route("/tools")
def tools():
    return render_template("tools.html")


@core_bp.route("/health")
def health():
    return {"status": "ok", "app": "FLD System Builder"}
