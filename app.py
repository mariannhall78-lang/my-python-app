import os
from flask import Flask, render_template, send_from_directory

AZURE_ROOT = "/home/site/wwwroot"
TEMPLATE_DIR = os.path.join(AZURE_ROOT, "templates")
STATIC_DIR = os.path.join(AZURE_ROOT, "static")

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/files/<path:filename>")
def files(filename):
    return send_from_directory(AZURE_ROOT, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
