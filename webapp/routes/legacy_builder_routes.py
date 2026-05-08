from flask import Blueprint, request

from flask_app import app as legacy_app


legacy_builder_bp = Blueprint("legacy_builder", __name__)


def normalize_legacy_html(html):
    # Force every legacy form post to come back to the Flask bridge route.
    html = html.replace('<form method="post">', '<form method="post" action="/builder-v27">')
    html = html.replace("<form method='post'>", "<form method='post' action='/builder-v27'>")
    html = html.replace('<form method="POST">', '<form method="POST" action="/builder-v27">')
    html = html.replace('action="/"', 'action="/builder-v27"')
    html = html.replace("action='/'", "action='/builder-v27'")
    html = html.replace('action=""', 'action="/builder-v27"')
    html = html.replace('action="/builder-v27/builder-v27"', 'action="/builder-v27"')
    return html


@legacy_builder_bp.route("/builder-v27", methods=["GET", "POST"])
def builder_v27():
    with legacy_app.test_request_context("/", method=request.method, data=request.form):
        response = legacy_app.full_dispatch_request()

    if isinstance(response, str):
        return normalize_legacy_html(response)

    if hasattr(response, "get_data"):
        html = response.get_data(as_text=True)
        response.set_data(normalize_legacy_html(html))
        return response

    return response
