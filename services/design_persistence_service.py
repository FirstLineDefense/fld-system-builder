from repositories.design_repository import (
    save_primary_design,
    load_primary_design,
)


def save_design(primary):
    return save_primary_design(
        primary
    )


def load_design():
    return load_primary_design()
