from datetime import datetime
import uuid


def generate_proposal_metadata(
    client_name="Client",
    property_address="Property Address Pending",
):
    timestamp = datetime.now()

    proposal_id = (
        "FLD-"
        + timestamp.strftime("%Y%m%d")
        + "-"
        + str(uuid.uuid4())[:8].upper()
    )

    return {
        "proposal_id": proposal_id,
        "generated_date": timestamp.strftime("%B %d, %Y"),
        "generated_time": timestamp.strftime("%I:%M %p"),
        "client_name": client_name,
        "property_address": property_address,
        "prepared_by": "First Line Defense",
        "proposal_status": "Preliminary System Design",
    }
