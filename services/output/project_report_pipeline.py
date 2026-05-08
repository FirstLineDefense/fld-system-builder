
from services.pricing.pricing_engine import generate_pricing_summary
from services.output.project_report_model import ProjectReport


def generate_project_report_package(project=None, package=None, **kwargs):
    data = project or package or kwargs or {}
    if not isinstance(data, dict):
        data = {}

    pricing = generate_pricing_summary(data)

    html_report = f'''
    <h1>FLD Project Report</h1>
    <h2>Pricing Summary</h2>
    <pre>{pricing}</pre>
    '''

    return ProjectReport(
        meta={"name": "FLD Project Report"},
        pricing=pricing,
        html_report=html_report
    )
