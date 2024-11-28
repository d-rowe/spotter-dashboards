from flask import Flask
import ingest

app = Flask(__name__)

@app.route("/")
def index():
    ingest.run();
    return "Hello, World!"
