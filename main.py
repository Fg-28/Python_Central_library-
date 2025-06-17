from flask import Flask, request, Response
from datetime import datetime
import os
import requests

app = Flask(__name__)
GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycby_QpaF75QTHhXWxpNPmjsnylyM_8RBDGIbHT3-FygJPGLs1kikJDEkufHHe18kJ1o7vg/exec"
PASSWORD = "FG@RL5851"

@app.route("/get_script")
def get_script():
    script_name = request.args.get("script", "").strip()
    guid = request.args.get("guid", "").strip()
    password = request.args.get("password", "").strip()

    if not script_name or not guid or not password:
        return Response("Missing script, guid or password", 400)

    if password != PASSWORD:
        return Response("AUTH FAILED: Wrong password.", 403)

    # Step 1: Validate with Google Sheet
    try:
        res = requests.get(GOOGLE_SCRIPT_URL, params={"script": script_name, "guid": guid})
        if res.status_code != 200:
            return Response("Google Sheet validation failed", 502)

        data = res.json()
        if data.get("shutdown", False):
            return Response("SHUTDOWN", 403)
        if not data.get("run", False):
            return Response("NOT ALLOWED TO RUN", 403)

    except Exception as e:
        return Response(f"Google validation error: {str(e)}", 500)

    print(f"[{datetime.utcnow()}] Script: {script_name} | GUID: {guid} | AUTHORIZED")
    return Response("AUTHORIZED", mimetype="text/plain")

@app.route("/")
def home():
    return "Python validation server is running."

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
