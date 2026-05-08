from webapp.design_api import (
    get_design_report,
)


def handle_design_report_request(
    primary
):
    return get_design_report(
        primary
    )
