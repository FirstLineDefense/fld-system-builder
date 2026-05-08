from pathlib import Path


def _build_links(files, route_prefix):
    if not files:
        return "<p>No files yet.</p>"

    items = []

    for file_path in files:
        name = Path(file_path).name
        items.append(
            f'<li><a href="{route_prefix}/{name}">{name}</a></li>'
        )

    return "<ul>" + "\n".join(items) + "</ul>"


def build_snapshot_index_html(snapshots):
    html_links = _build_links(
        snapshots.get("html", []),
        "/proposal-snapshots/html",
    )

    json_links = _build_links(
        snapshots.get("json", []),
        "/proposal-snapshots/json",
    )

    pdf_links = _build_links(
        snapshots.get("pdf", []),
        "/proposal-snapshots/pdf",
    )

    return f"""
    <html>
    <head>
        <title>Proposal Snapshots</title>
        <link rel="stylesheet" href="/static/css/proposal_report.css">
    </head>
    <body>
        <div class="report-container">
            <h1>Proposal Snapshots</h1>

            <h2>HTML Snapshots</h2>
            {html_links}

            <h2>JSON Snapshots</h2>
            {json_links}

            <h2>PDF Snapshots</h2>
            {pdf_links}
        </div>
    </body>
    </html>
    """
