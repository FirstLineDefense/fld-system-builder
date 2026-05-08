from renderers.page_renderer import (
    build_standalone_page,
)


def build_saved_projects_page(
    projects
):
    rows = ""

    for project in projects:
        rows += f"""
<tr>
<td>{project.get("id", "")}</td>
<td>{project.get("project_name", "")}</td>
<td>{project.get("version_label", "")}</td>
<td>{project.get("status", "")}</td>
<td>{project.get("client_name", "")}</td>
<td>{project.get("property_name", "")}</td>

<td>
<a href="/projects/{project.get('id')}">
View
</a>
</td>

<td>
<form method="POST"
action="/projects/{project.get('id')}/delete">

<button type="submit">
Delete
</button>

</form>
</td>

</tr>
"""

    body = f"""
<h2>Saved Projects</h2>

<table>

<tr>
<th>ID</th>
<th>Project</th>
<th>Version</th>
<th>Status</th>
<th>Client</th>
<th>Property</th>
<th>View</th>
<th>Delete</th>
</tr>

{rows}

</table>
"""

    return build_standalone_page(
        "Saved Projects",
        body
    )


def build_saved_project_detail_page(
    project
):
    body = f"""
<h2>
{project.get("project_name", "")}
</h2>

<table>

<tr>
<th>Field</th>
<th>Value</th>
</tr>

<tr>
<td>ID</td>
<td>{project.get("id", "")}</td>
</tr>

<tr>
<td>Version</td>
<td>{project.get("version_label", "")}</td>
</tr>

<tr>
<td>Status</td>
<td>{project.get("status", "")}</td>
</tr>

<tr>
<td>Client</td>
<td>{project.get("client_name", "")}</td>
</tr>

<tr>
<td>Property</td>
<td>{project.get("property_name", "")}</td>
</tr>

<tr>
<td>Revision Notes</td>
<td>{project.get("revision_notes", "")}</td>
</tr>

<tr>
<td>Site Notes</td>
<td>{project.get("site_notes", "")}</td>
</tr>

<tr>
<td>Designer Notes</td>
<td>{project.get("designer_notes", "")}</td>
</tr>

</table>

<p>
<a href="/">
Back to Builder
</a>
</p>
"""

    return build_standalone_page(
        "Project Detail",
        body
    )
