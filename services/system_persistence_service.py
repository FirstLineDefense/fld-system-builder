def persist_system_if_requested(
    form,
    metadata,
    input_data,
    result,
    save_system_design,
):
    save_requested = (
        form.get("save_project", ["no"])[0] == "yes"
    )

    if not save_requested:
        return ""

    saved_id = save_system_design(
        metadata["display_name"],
        input_data,
        result,
        project_name=metadata["project_name"],
        version_label=metadata["version_label"],
        revision_notes=metadata["revision_notes"],
        status=metadata["status"],
        client_name=metadata["client_name"],
        property_name=metadata["property_name"],
        site_notes=metadata["site_notes"],
        designer_notes=metadata["designer_notes"],
        parent_id=metadata["parent_id"],
    )

    return (
        f'<div class="message">'
        f'Saved project version: '
        f'{metadata["display_name"]} '
        f'(ID {saved_id})'
        f'</div>'
    )
