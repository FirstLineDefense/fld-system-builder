def enhance_nav(page):
    return page.replace(
        '<a href="/components">Component Manager</a>',
        '<a href="/components">Component Manager</a> | <a href="/pump-curves">Pump Curves</a> | <a href="/optimizer">Optimizer</a> | <a href="/projects">Saved Projects</a>'
    )


def build_standalone_page(
    title,
    body
):
    return f"""
<!DOCTYPE html>
<html>
<head>
<title>{title}</title>

<style>
body {{
    font-family: Arial, sans-serif;
    margin: 40px;
    max-width: 1500px;
}}

label {{
    display: block;
    margin-top: 12px;
    font-weight: bold;
}}

input, select, textarea {{
    width: 420px;
    padding: 8px;
    margin-top: 4px;
}}

table {{
    border-collapse: collapse;
    width: 100%;
    margin-top: 15px;
    margin-bottom: 50px;
}}

td, th {{
    border: 1px solid #ccc;
    padding: 8px;
    text-align: left;
    vertical-align: top;
}}

th {{
    background: #eee;
}}

button {{
    padding: 8px 12px;
    margin-top: 8px;
}}

.message {{
    background: #e8f5e9;
    padding: 12px;
    border: 1px solid #999;
    margin-bottom: 20px;
}}

.warning {{
    background: #fff8e1;
    padding: 12px;
    border: 1px solid #c9a227;
    margin-bottom: 20px;
}}

.result {{
    margin-top: 30px;
    padding: 20px;
    border: 1px solid #ccc;
    background: #f7f7f7;
}}

pre {{
    white-space: pre-wrap;
    background: #f7f7f7;
    padding: 15px;
    border: 1px solid #ccc;
}}

.codehint {{
    font-family: monospace;
    background: #f7f7f7;
    padding: 10px;
    border: 1px solid #ccc;
    width: 420px;
}}

.curve-card {{
    padding: 18px;
    border: 1px solid #ccc;
    background: #fafafa;
    margin-top: 20px;
}}
</style>

</head>

<body>

<h1>{title}</h1>

<p>
<a href="/">System Builder</a> |
<a href="/components">Component Manager</a> |
<a href="/pump-curves">Pump Curves</a> |
<a href="/optimizer">Optimizer</a> |
<a href="/projects">Saved Projects</a>
</p>

{body}

</body>
</html>
"""
