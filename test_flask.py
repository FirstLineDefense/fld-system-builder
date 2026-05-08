from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "FLD TEST OK"

if __name__ == "__main__":
    app.run(port=5010)
