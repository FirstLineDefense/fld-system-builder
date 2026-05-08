def build_pump_select_options(pumps, selected_pump_name=""):
    html = ""

    for pump in pumps:
        pump_name = getattr(pump, "name", "")

        selected = ""
        if pump_name == selected_pump_name:
            selected = "selected"

        html += (
            f'<option value="{pump_name}" {selected}>'
            f'{pump_name}'
            f'</option>'
        )

    return html


def build_curve_preview_section(selected_pump_name):
    if not selected_pump_name:
        return ""

    return f"""
<h2>Curve Preview</h2>

<div class="info-card">
Currently selected pump:
<strong>{selected_pump_name}</strong>
</div>
"""
