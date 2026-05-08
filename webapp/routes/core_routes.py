from flask import Blueprint, render_template, redirect

core_bp = Blueprint("core", __name__)


@core_bp.route("/")
def dashboard():
    return redirect("/optimizer")


@core_bp.route("/tools")
def tools():
    return render_template("tools.html")


@core_bp.route("/health")
def health():
    return "ok", 200
