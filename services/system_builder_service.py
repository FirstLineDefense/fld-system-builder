from domain.schemas import (
    build_system_input_dto,
    validate_system_input_dto,
)

def build_project_metadata(form):
    project_name = form.get("project_name", [""])[0].strip()
    version_label = form.get("version_label", [""])[0].strip()

    status = form.get("status", ["Draft"])[0]

    client_name = form.get("client_name", [""])[0].strip()
    property_name = form.get("property_name", [""])[0].strip()

    revision_notes = form.get("revision_notes", [""])[0]
    site_notes = form.get("site_notes", [""])[0]
    designer_notes = form.get("designer_notes", [""])[0]

    parent_id_raw = form.get("parent_id", [""])[0]
    parent_id = int(parent_id_raw) if parent_id_raw else None

    if not project_name:
        project_name = "Untitled FLD System Design"

    if not version_label:
        version_label = "V1"

    display_name = f"{project_name} {version_label}"

    return {
        "project_name": project_name,
        "version_label": version_label,
        "status": status,
        "client_name": client_name,
        "property_name": property_name,
        "revision_notes": revision_notes,
        "site_notes": site_notes,
        "designer_notes": designer_notes,
        "parent_id": parent_id,
        "display_name": display_name,
    }


def build_saved_stub(metadata):
    return {
        "project_name": metadata["project_name"],
        "version_label": metadata["version_label"],
        "revision_notes": metadata["revision_notes"],
        "status": metadata["status"],
        "client_name": metadata["client_name"],
        "property_name": metadata["property_name"],
        "site_notes": metadata["site_notes"],
        "designer_notes": metadata["designer_notes"],
        "id": metadata["parent_id"] or "",
    }

def normalize_and_validate_system_input(raw_data):
    dto = build_system_input_dto(raw_data)
    valid, errors = validate_system_input_dto(dto)

    if not valid:
        raise ValueError(f'System DTO validation failed: {errors}')

    return dto
