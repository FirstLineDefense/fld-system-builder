from flask import Flask

flask_app = Flask(__name__)

PAGE_STYLE = """
<style>
    body {
        font-family: Arial, sans-serif;
        background: #f5f7f9;
        margin: 0;
        padding: 40px;
        color: #1f2933;
    }
    .wrap {
        max-width: 900px;
        margin: 0 auto;
    }
    h1 {
        margin-bottom: 5px;
    }
    .subtitle {
        color: #52616b;
        margin-bottom: 30px;
    }
    .grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 18px;
    }
    .card {
        background: white;
        border: 1px solid #d9e2ec;
        border-radius: 12px;
        padding: 22px;
        text-decoration: none;
        color: #1f2933;
        box-shadow: 0 2px 6px rgba(0,0,0,0.06);
    }
    .card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.12);
    }
    .card h2 {
        margin: 0 0 10px 0;
        font-size: 20px;
    }
    .card p {
        margin: 0;
        color: #52616b;
        line-height: 1.4;
    }
</style>
"""

@flask_app.route("/")
def home():
    return f"""
    <html>
    <head>
        <title>FLD System Builder</title>
        {PAGE_STYLE}
    </head>
    <body>
        <div class="wrap">
            <h1>FLD System Builder</h1>
            <p class="subtitle">Control dashboard for FLD tools and reports.</p>

            <div class="grid">
                <a class="card" href="/tools">
                    <h2>Tools Console</h2>
                    <p>Access the main FLD tool set.</p>
                </a>

                <a class="card" href="/components">
                    <h2>Component Library</h2>
                    <p>View and manage system components.</p>
                </a>

                <a class="card" href="/optimizer">
                    <h2>Optimizer</h2>
                    <p>Run optimization and scoring tools.</p>
                </a>

                <a class="card" href="/project-report">
                    <h2>Project Report</h2>
                    <p>Open report and proposal outputs.</p>
                </a>
            </div>
        </div>
    </body>
    </html>
    """

@flask_app.route("/tools")
def tools():
    return "<h1>TOOLS OK</h1><p><a href='/'>Back to Dashboard</a></p>"

@flask_app.route("/components")
def components():
    return "<h1>COMPONENTS OK</h1><p><a href='/'>Back to Dashboard</a></p>"

@flask_app.route("/optimizer")
def optimizer():
    return "<h1>OPTIMIZER OK</h1><p><a href='/'>Back to Dashboard</a></p>"

@flask_app.route("/project-report")
def project_report():
    return "<h1>PROJECT REPORT OK</h1><p><a href='/'>Back to Dashboard</a></p>"

if __name__ == "__main__":
    flask_app.run(port=5010)
