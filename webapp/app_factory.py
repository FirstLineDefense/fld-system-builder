from pathlib import Path
from flask import Flask

from webapp.routes.core_routes import core_bp
from webapp.routes.component_routes import component_bp
from webapp.routes.optimizer_routes import optimizer_bp
from webapp.routes.project_routes import project_bp
from webapp.routes.report_routes import report_bp
from webapp.routes.legacy_builder_routes import legacy_builder_bp
from webapp.routes.workflow_routes import workflow_bp


def create_app():
    project_root = Path(__file__).resolve().parent.parent

    app = Flask(
        __name__,
        template_folder=str(project_root / "templates"),
        static_folder=str(project_root / "static"),
    )

    app.register_blueprint(core_bp)
    app.register_blueprint(component_bp)
    app.register_blueprint(optimizer_bp)
    app.register_blueprint(project_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(legacy_builder_bp)
    app.register_blueprint(workflow_bp)

    @app.template_filter("money")
    def money(value):
        try:
            return "${:,.2f}".format(float(value or 0))
        except:
            return "$0.00"

    return app
