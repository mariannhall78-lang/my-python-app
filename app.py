import os
from flask import Flask, send_from_directory, render_template

AZURE_ROOT = "/home/site/wwwroot"
STATIC_DIR = os.path.join(AZURE_ROOT, "static")
TEMPLATE_DIR = os.path.join(AZURE_ROOT, "templates")

app = Flask(__name__, static_folder=STATIC_DIR, template_folder=TEMPLATE_DIR)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/files/<path:filename>")
def files(filename):
    return send_from_directory(AZURE_ROOT, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
