from renderers.proposal.header_renderer import (
    build_proposal_header_html,
)

from renderers.proposal.footer_renderer import (
    build_proposal_footer_html,
)


def compose_project_report_page(
    title,
    body_html,
    controls_html="",
):
    header_html = build_proposal_header_html(title)

    footer_html = build_proposal_footer_html()

    return f"""
    <html>
    <head>
        <title>{title}</title>

        <link
            rel="stylesheet"
            href="/static/css/proposal_report.css"
        >
    </head>

    <body>
        <div class="report-container">

            {header_html}

            <div class="report-controls">
                {controls_html}
            </div>

            {body_html}

            {footer_html}

        </div>
    </body>
    </html>
    """
