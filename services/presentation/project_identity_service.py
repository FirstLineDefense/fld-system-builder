from datetime import datetime


def generate_project_identity():
    return {
        "project_name": "Topanga Canyon Wildfire Resiliency System",
        "client_name": "Demo Client",
        "proposal_revision": "Rev A",
        "proposal_status": "Preliminary Design",
        "designer": "FLD System Builder",
        "generated_date": datetime.now().strftime("%B %d, %Y"),
    }
