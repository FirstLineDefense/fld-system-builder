from services.design_viewmodel_service import (
    build_design_viewmodel,
)

from renderers.constraint_violation_renderer import (
    build_constraint_violation_html,
)


def generate_design_report(
    primary
):
    viewmodel = build_design_viewmodel(
        primary
    )

    html = build_constraint_violation_html(
        primary,
        viewmodel.get(
            "violations",
            []
        )
    )

    return {
        "viewmodel": viewmodel,
        "html": html,
    }
