from flask import Blueprint, request

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
    from app import build_system_builder_page

    if request.method == "GET":
        return normalize_legacy_html(build_system_builder_page())

    return "Legacy builder POST bridge not restored yet.", 501
