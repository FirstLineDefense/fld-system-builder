from services.design_analysis_service import (
    analyze_design,
)

from services.design_persistence_service import (
    save_design,
    load_design,
)


def analyze_primary(primary):
    return analyze_design(
        primary
    )


def save_primary(primary):
    return save_design(
        primary
    )


def load_primary():
    return load_design()
