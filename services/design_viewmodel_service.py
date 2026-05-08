from services.application_service import (
    analyze_primary,
)


def build_design_viewmodel(
    primary
):
    analysis = analyze_primary(
        primary
    )

    return {
        "primary": primary,
        "violations": analysis.get(
            "violations",
            []
        ),
        "score": analysis.get(
            "score",
            {}
        ),
        "auto_apply": analysis.get(
            "auto_apply",
            {}
        ),
    }
