from pathlib import Path


def detect_pdf_engine():
    try:
        import weasyprint  # noqa: F401

        return {
            "available": True,
            "engine": "weasyprint",
        }

    except Exception as exc:
        return {
            "available": False,
            "engine": None,
            "error": str(exc),
        }


def create_pdf_placeholder_from_html(html_path):
    source = Path(html_path)

    pdf_path = Path("exports/proposals/pdf") / source.with_suffix(".pdf").name

    pdf_path.write_text(
        "PDF PLACEHOLDER\n\n"
        f"Source HTML: {source}\n\n"
        "WeasyPrint is not available yet because macOS native libraries are not linked.\n"
    )

    return str(pdf_path)
